"""Server-rendered multi-page UI. No JavaScript framework required."""
from pathlib import Path
from urllib.parse import parse_qs, urlencode
from collections import defaultdict
from math import ceil
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.dal.semantic_store import ROOT, Store, initialize, PREFIX
from src.biz.semantic_services import Services,KINDS,TYPES,QUERIES,Validation

RUNTIME=ROOT/'data/preprocessed/semantic_runtime.rdf'

def create_app(path=RUNTIME, store=None):
 path=Path(path)
 if store is None:
  if not path.exists(): initialize(path)
  store=Store(path)
 service=Services(store)
 app=FastAPI(title='ProduCast Semantic',docs_url=None,redoc_url=None)
 here=Path(__file__).parent
 app.mount('/static',StaticFiles(directory=here/'semantic_static'),name='static')
 env=Environment(loader=FileSystemLoader(here/'semantic_templates'),autoescape=select_autoescape(['html']))
 def render(template,request,**ctx):
  return HTMLResponse(env.get_template(template).render(kinds=KINDS,types=TYPES,active=ctx.pop('active',''),message=request.query_params.get('message',''),error=request.query_params.get('error',''),**ctx))
 def catalog():
  # Fetch each resource type once via SPARQL, then build view indexes.
  data={k:service.records(k) for k in KINDS}
  byid={k:{r['id']:r for r in rows} for k,rows in data.items()}
  cast=defaultdict(list); acting=defaultdict(list); directing=defaultdict(list); camera=defaultdict(list); awards=defaultdict(list); film_awards=defaultdict(list); studios=defaultdict(list); pairs=defaultdict(dict)
  for m in data['movies']:
   for k,_ in m['links'].get('directedBy',[]): directing[k].append(m)
   for k,_ in m['links'].get('filmedBy',[]): camera[k].append(m)
   for k,_ in m['links'].get('producedBy',[]): studios[k].append(m)
  for r in data['casting']:
   for mid,_ in r['links'].get('belongsTo',[]):
    m=byid['movies'].get(mid)
    if not m: continue
    for pid,name in r['links'].get('filledBy',[]):
     item={'movie':m,'role':r,'person':byid['talent'].get(pid)}; cast[mid].append(item); acting[pid].append(item)
     for did,_ in m['links'].get('directedBy',[]):
      if pid!=did: pairs[(pid,did)][mid]=m
  for a in data['awards']:
   for k,_ in a['links'].get('receivedBy',[]): awards[k].append(a)
   for k,_ in a['links'].get('awardedFor',[]): film_awards[k].append(a)
  collaborations=[{'actor':byid['talent'][a],'director':byid['talent'][d],'films':list(ms.values()),'count':len(ms)} for (a,d),ms in pairs.items() if a in byid['talent'] and d in byid['talent']]
  collaborations.sort(key=lambda x:(-x['count'],x['actor']['label'],x['director']['label']))
  return dict(data=data,byid=byid,cast=cast,acting=acting,directing=directing,camera=camera,awards=awards,film_awards=film_awards,studios=studios,collaborations=collaborations)
 def back(url,**params):return RedirectResponse(url+'?'+urlencode(params),303)
 def kindcheck(kind):
  if kind not in KINDS: raise HTTPException(404)
 @app.get('/')
 def home(request:Request):
  c=catalog(); stats={'movies':len(c['data']['movies']),'actors':sum('Actor' in r['types'] for r in c['data']['talent']),'directors':sum('Director' in r['types'] for r in c['data']['talent']),'awards':len(c['data']['awards'])}
  titles=['Oppenheimer','The Revenant','La La Land','The Dark Knight']; featured=sorted((r for r in c['data']['movies'] if r['label'] in titles),key=lambda r:titles.index(r['label']))
  return render('home.html',request,active='home',stats=stats,featured=featured or c['data']['movies'][:4],pairs=c['collaborations'][:3])
 @app.get('/explore')
 def explore(request:Request,q:str='',repeat:bool=False):
  c=catalog(); pairs=[p for p in c['collaborations'] if (not repeat or p['count']>1) and (not q or q.casefold() in (' '.join([p['actor']['label'],p['director']['label']]+[m['label'] for m in p['films']])).casefold())]
  return render('explore.html',request,active='explore',pairs=pairs,q=q,repeat=repeat)
 @app.get('/queries')
 def queries(request:Request,query:str='cast'):
  if query not in QUERIES: query='cast'
  title,q=QUERIES[query]; rows=service.store.select(q)
  return render('queries.html',request,active='queries',queries=QUERIES,selected=query,title=title,code=PREFIX+q,rows=rows,headers=list(rows[0]) if rows else [],issues=service.diagnostics())
 @app.get('/export.rdf')
 def export():return Response(store.all_graph().serialize(format='xml'),media_type='application/rdf+xml',headers={'Content-Disposition':'attachment; filename=producast-graph.rdf'})
 @app.get('/{kind}')
 def listing(request:Request,kind:str,q:str='',role:str='',page:int=1):
  kindcheck(kind); c=catalog(); matches=service.records(kind,q[:255],role) if q or role else c['data'][kind]
  pages=max(1,ceil(len(matches)/12)); page=max(1,min(page,pages)); total=len(matches)
  def pageurl(n):return '/'+kind+'?'+urlencode({'q':q,'role':role,'page':n})
  return render('listing.html',request,active=kind,kind=kind,records=matches[(page-1)*12:page*12],q=q,role=role,c=c,total=total,page=page,pages=pages,prev=pageurl(page-1),next=pageurl(page+1))
 @app.get('/{kind}/new')
 def new(request:Request,kind:str):
  kindcheck(kind); return form(request,kind,None)
 def form(request,kind,rec):
  return render('form.html',request,active=kind,kind=kind,rec=rec,options={p:service.options(c) for p,_,c,_ in KINDS[kind][3]})
 @app.get('/{kind}/{key}/edit')
 def edit(request:Request,kind:str,key:str):
  kindcheck(kind); rec=service.get(kind,key)
  if not rec:raise HTTPException(404)
  return form(request,kind,rec)
 @app.get('/{kind}/{key}')
 def detail(request:Request,kind:str,key:str):
  kindcheck(kind); rec=service.get(kind,key)
  if not rec:raise HTTPException(404)
  c=catalog(); return render('detail.html',request,active=kind,kind=kind,rec=rec,c=c)
 @app.post('/{kind}/save')
 async def save(request:Request,kind:str):
  kindcheck(kind); body=await request.body()
  if len(body)>20000:raise HTTPException(413)
  data=parse_qs(body.decode(),keep_blank_values=True); key=data.get('id',[''])[0] or None
  try: key=service.save(kind,data,key); return back(f'/{kind}/{key}',message='Changes saved.')
  except Validation as e:return back(f'/{kind}/{key}/edit' if key else f'/{kind}/new',error=str(e))
 @app.post('/{kind}/{key}/delete')
 def delete(kind:str,key:str):
  kindcheck(kind)
  try: service.delete(kind,key);return back('/'+kind,message='Entry removed.')
  except Validation as e:return back('/'+kind+'/'+key,error=str(e))
 return app
