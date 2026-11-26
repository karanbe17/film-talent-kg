"""Domain validation and safe SPARQL operations for the semantic UI."""
from rdflib import URIRef, Literal, RDF
from uuid import uuid4
from datetime import date
from decimal import Decimal,InvalidOperation
import re
from src.dal.semantic_store import PC, PREFIX, PROPS, LINKS, lit

# key -> class, display label, scalar fields, relationship fields
KINDS={
 'movies':('Movie','Movies', [('title','Title',True),('genre','Genre',True),('releaseYear','Release year',False),('releaseDate','Release date',False),('duration','Duration (minutes)',False),('budget','Budget',False),('boxOfficeRevenue','Box office',False)], [('producedBy','Studio','Studio',True),('directedBy','Directors','Director',False),('filmedBy','Camera crew','CameraMan',False)]),
 'talent':('Person','Talent',[('name','Full name',True),('birthDate','Birth date',False)],[]),
 'studios':('Studio','Studios',[('studioName','Studio name',True),('hq','Headquarters',False)],[]),
 'awards':('Award','Awards',[('awardName','Award name',True),('category','Category',True),('year','Year',True)],[('receivedBy','Recipient','Person',True),('awardedFor','Film','Movie',False)]),
 'casting':('PerformanceRole','Casting',[('characterName','Character name',True),('roleType','Role type',False),('billingOrder','Billing order',False)],[('belongsTo','Movie','Movie',True),('filledBy','Actor','Actor',True)])}
LABEL={'Person':'name','Actor':'name','Director':'name','CameraMan':'name','Movie':'title','Studio':'studioName','Award':'awardName','PerformanceRole':'characterName'}
TYPES=['Actor','Director','CameraMan']
class Validation(ValueError): pass

def local(s): return str(s).split('#')[-1]
def uri(key):
 if not re.fullmatch(r'[a-zA-Z0-9_-]{1,100}',key or ''): raise Validation('Invalid resource identifier.')
 return PC[key]
def text_value(p,v):
 v=v.strip()
 if len(v)>255: raise Validation('Fields must contain at most 255 characters.')
 if not v: return None
 try:
  if p in ('releaseDate','birthDate'): v=date.fromisoformat(v).isoformat()
  if p in ('duration','billingOrder'):
   v=int(v)
   if v<1: raise ValueError()
  if p in ('budget','boxOfficeRevenue'):
   v=Decimal(v)
   if not v.is_finite() or v<0: raise ValueError()
  if p in ('year','releaseYear') and (not re.fullmatch(r'\d{4}',v) or not 1800<=int(v)<=2200): raise ValueError()
  if p=='roleType' and v not in ('Lead','Supporting','Cameo'): raise ValueError()
 except (ValueError,InvalidOperation): raise Validation(f'Invalid value for {p}.')
 return lit(p,v)

class Services:
 def __init__(self,store): self.store=store
 def options(self,c):
  return [(local(r['s']),str(r['label'])) for r in self.store.select(f'SELECT ?s ?label WHERE {{ ?s a pc:{c}; pc:{LABEL[c]} ?label }} ORDER BY LCASE(STR(?label))')]
 def records(self,kind,q='',role=''):
  c,_,fields,links=KINDS[kind]; label=LABEL[c]
  # A SELECT retrieves all predicates; regroup rows without losing multivalued properties.
  filt='';
  if q: filt=f'FILTER(CONTAINS(LCASE(STR(?label)), LCASE({Literal(q).n3()})) || EXISTS {{ ?s ?searchP ?searchV . FILTER(?searchP NOT IN (pc:source,pc:referenceUrl)) FILTER(CONTAINS(LCASE(STR(?searchV)), LCASE({Literal(q).n3()}))) }} || EXISTS {{ ?s ?searchP ?other . ?other ?lp ?searchV . FILTER(isLiteral(?searchV) && CONTAINS(LCASE(STR(?searchV)), LCASE({Literal(q).n3()}))) }})'
  if kind=='talent' and role in TYPES: filt+=f'\n?s a pc:{role} .'
  rows=self.store.select(f'SELECT ?s ?label ?p ?o ?linked WHERE {{ ?s a pc:{c}; pc:{label} ?label; ?p ?o . OPTIONAL {{ ?o (pc:name|pc:title|pc:studioName|pc:awardName|pc:characterName) ?linked }} {filt} }} ORDER BY LCASE(STR(?label))')
  result={}
  for r in rows:
   k=local(r['s']); rec=result.setdefault(k,{'id':k,'label':str(r['label']),'values':{},'links':{},'types':[]})
   p=local(r['p']); o=r['o']
   if r['p']==RDF.type: rec['types'].append(local(o))
   elif isinstance(o,URIRef): rec['links'].setdefault(p,[]).append((local(o),str(r.get('linked',local(o)))))
   else: rec['values'][p]=str(o)
  return list(result.values())
 def get(self,kind,key):
  return next((r for r in self.records(kind) if r['id']==key),None)
 def save(self,kind,form,key=None):
  c,_,fields,links=KINDS[kind]; s=uri(key) if key else PC['item-'+uuid4().hex]; values=[]; types=[c]
  for p,_,required in fields:
   v=text_value(p,form.get(p,[''])[0]);
   if required and v is None: raise Validation(f'{p} is required.')
   if v is not None: values.append((PC[p],v))
  if kind=='talent': types+=list(dict.fromkeys(t for t in form.get('roles',[]) if t in TYPES))
  def modify(g):
   if key and (s,RDF.type,PC[c]) not in g: raise Validation('Record not found.')
   for p,_,target,required in links:
    keys=list(dict.fromkeys(v for v in form.get(p,[]) if v))
    if required and len(keys)!=1: raise Validation(f'Choose exactly one {target}.')
    if p=='awardedFor' and len(keys)>1: raise Validation('Choose at most one film for an award occurrence.')
    for k in keys:
     obj=uri(k)
     if (obj,RDF.type,PC[target]) not in g: raise Validation(f'Invalid {target} selection.')
     values.append((PC[p],obj))
   # Protect subclass membership used by existing credits.
   if kind=='talent' and key:
    for p,t in [('filledBy','Actor'),('directedBy','Director'),('filmedBy','CameraMan')]:
     if t not in types and any(g.subjects(PC[p],s)): raise Validation(f'Cannot remove {t}: existing credits reference this person.')
   # Preserve previous provenance for edited records; new records are user-entered.
   source=next(g.objects(s,PC.source),lit('source','User-entered data'))
   values.extend((PC.referenceUrl,v) for v in g.objects(s,PC.referenceUrl))
   triples=[(RDF.type,PC[t]) for t in types]+values+[(PC.source,source)]
   if key: g.update(PREFIX+f'DELETE WHERE {{ {s.n3()} ?p ?o }}')
   g.update(PREFIX+'INSERT DATA { '+ ' '.join(f'{s.n3()} {p.n3()} {v.n3()} .' for p,v in triples)+' }')
   return local(s)
  return self.store.change(modify)
 def delete(self,kind,key):
  s=uri(key); c=KINDS[kind][0]
  def modify(g):
   if (s,RDF.type,PC[c]) not in g: raise Validation('Record not found.')
   if kind=='studios' and any(g.subjects(PC.producedBy,s)): raise Validation('Studio is in use. Reassign its movies first.')
   # Dependent roles and award records would become invalid; remove them with the parent.
   children=set(g.subjects(PC.belongsTo,s))|set(g.subjects(PC.filledBy,s))|set(g.subjects(PC.receivedBy,s))|set(g.subjects(PC.awardedFor,s))
   for child in children|{s}:
    g.update(PREFIX+f'DELETE WHERE {{ {child.n3()} ?p ?o }}'); g.update(PREFIX+f'DELETE WHERE {{ ?s ?p {child.n3()} }}')
  self.store.change(modify)
 def diagnostics(self):
  return self.store.select('''SELECT ?title ?issue WHERE { ?m a pc:Movie; pc:title ?title . { FILTER NOT EXISTS { ?m pc:directedBy ?d } BIND("Missing director" AS ?issue) } UNION { FILTER NOT EXISTS { ?r pc:belongsTo ?m } BIND("Missing cast" AS ?issue) } UNION { FILTER NOT EXISTS { ?m pc:producedBy ?s } BIND("Missing studio" AS ?issue) } } ORDER BY ?title ?issue''')
QUERIES={
 'cast':('Cast by film','SELECT ?movie ?actor ?character ?type WHERE { ?r a pc:PerformanceRole; pc:belongsTo/pc:title ?movie; pc:filledBy/pc:name ?actor; pc:characterName ?character . OPTIONAL { ?r pc:roleType ?type } } ORDER BY ?movie ?actor'),
 'collaborations':('Actor–director collaboration counts','SELECT ?actor ?director (COUNT(DISTINCT ?m) AS ?films) WHERE { ?r pc:filledBy ?a; pc:belongsTo ?m . ?m pc:directedBy ?d . ?a pc:name ?actor . ?d pc:name ?director } GROUP BY ?a ?d ?actor ?director ORDER BY DESC(?films)'),
 'studios':('Studio film counts','SELECT ?studio (COUNT(DISTINCT ?m) AS ?films) WHERE { ?s a pc:Studio; pc:studioName ?studio . OPTIONAL { ?m pc:producedBy ?s } } GROUP BY ?s ?studio ORDER BY DESC(?films)'),
 'awards':('Award recipients','SELECT ?person ?award ?category ?year ?film WHERE { ?a a pc:Award; pc:receivedBy/pc:name ?person; pc:awardName ?award; pc:category ?category; pc:year ?year . OPTIONAL { ?a pc:awardedFor/pc:title ?film } } ORDER BY DESC(?year) ?person'),
 'camera':('Camera crew credits','SELECT ?movie ?camera WHERE { ?m pc:title ?movie; pc:filmedBy/pc:name ?camera }'),
 'portfolio':('Talent with multiple professions','SELECT ?person (COUNT(DISTINCT ?role) AS ?professions) WHERE { ?p a pc:Person; pc:name ?person; a ?role . VALUES ?role {pc:Actor pc:Director pc:CameraMan} } GROUP BY ?p ?person HAVING(COUNT(DISTINCT ?role)>1)')}
