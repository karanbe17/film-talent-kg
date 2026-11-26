"""Embedded RDF triple store: RDFLib SPARQL engine and atomic RDF/XML persistence."""
from pathlib import Path
from threading import RLock
from rdflib import Graph, Namespace, URIRef, Literal, RDF, RDFS, OWL, XSD, BNode
from rdflib.collection import Collection
import sqlite3, hashlib, os
ROOT=Path(__file__).resolve().parents[2]
MODEL=ROOT/'src/dal/models/semantic'
PC=Namespace('https://github.com/karanbe17/film-talent-kg/ontology#')
PREFIX=f'PREFIX pc: <{PC}>\nPREFIX rdf: <{RDF}>\nPREFIX rdfs: <{RDFS}>\n'
CLASSES=['Person','Actor','Director','CameraMan','Movie','Studio','Award','PerformanceRole']
PROPS={
 'name':('Person',XSD.string),'birthDate':('Person',XSD.date),
 'title':('Movie',XSD.string),'genre':('Movie',XSD.string),'releaseDate':('Movie',XSD.date),'duration':('Movie',XSD.positiveInteger),'budget':('Movie',XSD.decimal),'boxOfficeRevenue':('Movie',XSD.decimal),
 'studioName':('Studio',XSD.string),'hq':('Studio',XSD.string),
 'awardName':('Award',XSD.string),'category':('Award',XSD.string),'year':('Award',XSD.gYear),
 'characterName':('PerformanceRole',XSD.string),'billingOrder':('PerformanceRole',XSD.positiveInteger),'roleType':('PerformanceRole',XSD.string),
 'releaseYear':('Movie',XSD.gYear),'referenceUrl':(None,XSD.anyURI),'source':(None,XSD.string)}
LINKS={'producedBy':('Movie','Studio'),'directedBy':('Movie','Director'),'filledBy':('PerformanceRole','Actor'),'belongsTo':('PerformanceRole','Movie'),'receivedBy':('Award','Person'),'filmedBy':('Movie','CameraMan'),'awardedFor':('Award','Movie')}

def new_graph():
 g=Graph(); g.bind('pc',PC); g.bind('owl',OWL); g.bind('xsd',XSD); return g

def ontology():
 g=new_graph(); g.add((URIRef(str(PC)[:-1]),RDF.type,OWL.Ontology))
 for c in CLASSES: g.add((PC[c],RDF.type,OWL.Class)); g.add((PC[c],RDFS.label,Literal(c)))
 for c in ['Actor','Director','CameraMan']: g.add((PC[c],RDFS.subClassOf,PC.Person))
 for p,(d,r) in PROPS.items():
  g.add((PC[p],RDF.type,OWL.DatatypeProperty)); g.add((PC[p],RDFS.range,r))
  if d: g.add((PC[p],RDFS.domain,PC[d]))
 for p,(d,r) in LINKS.items():
  g.add((PC[p],RDF.type,OWL.ObjectProperty)); g.add((PC[p],RDFS.domain,PC[d])); g.add((PC[p],RDFS.range,PC[r]))
 for p,q in [('directedBy','directs'),('filledBy','fills'),('belongsTo','hasRole'),('receivedBy','receives'),('filmedBy','films'),('producedBy','produces')]:
  d,r=LINKS[p]; g.add((PC[q],RDF.type,OWL.ObjectProperty)); g.add((PC[q],RDFS.domain,PC[r])); g.add((PC[q],RDFS.range,PC[d])); g.add((PC[p],OWL.inverseOf,PC[q]))
 def restriction(c,p,kind,n):
  b=BNode(); g.add((PC[c],RDFS.subClassOf,b)); g.add((b,RDF.type,OWL.Restriction)); g.add((b,OWL.onProperty,PC[p])); g.add((b,kind,Literal(n,datatype=XSD.nonNegativeInteger)))
 for c,p in [('Movie','producedBy'),('PerformanceRole','filledBy'),('PerformanceRole','belongsTo'),('Award','receivedBy')]: restriction(c,p,OWL.cardinality,1)
 restriction('Award','awardedFor',OWL.maxCardinality,1)
 for c,p in [('Movie','directedBy'),('Movie','hasRole'),('Director','directs'),('Studio','produces')]: restriction(c,p,OWL.minCardinality,1)
 for c,p in [('Person','name'),('Movie','title'),('Studio','studioName'),('Award','awardName'),('Award','category'),('Award','year'),('PerformanceRole','characterName')]: restriction(c,p,OWL.cardinality,1)
 # Role type is a relational extension; OWL enumeration of permitted literals.
 b=BNode(); l=BNode(); g.add((b,RDF.type,RDFS.Datatype)); g.add((b,OWL.oneOf,l)); Collection(g,l,[Literal(x,datatype=XSD.string) for x in ['Lead','Supporting','Cameo']]); g.add((PC.roleType,RDFS.range,b))
 return g

def studio_uri(name): return PC['studio-'+hashlib.sha256(name.strip().casefold().encode()).hexdigest()[:16]]
def lit(p,v): return Literal(v,datatype=PROPS[p][1])
def put(g,s,c,fields,source):
 g.add((s,RDF.type,PC[c])); g.add((s,PC.source,lit('source',source)))
 if c in ['Actor','Director','CameraMan']: g.add((s,RDF.type,PC.Person))
 for p,v in fields.items():
  if v is not None and v!='': g.add((s,PC[p],v if isinstance(v,URIRef) else lit(p,v)))

def convert(db):
 g=new_graph(); c=sqlite3.connect(f'{Path(db).resolve().as_uri()}?mode=ro',uri=True); c.row_factory=sqlite3.Row
 src='SQLite snapshot (Milestone 4)'
 try:
  for r in c.execute('SELECT * FROM Person'): put(g,PC[f'person-{r["Id"]}'],'Person',{'name':r['Name']},src)
  actors={r['Id']:PC[f'person-{r["PersonId"]}'] for r in c.execute('SELECT * FROM Actor')}; directors={r['Id']:PC[f'person-{r["PersonId"]}'] for r in c.execute('SELECT * FROM Director')}
  for s in actors.values(): g.add((s,RDF.type,PC.Actor))
  for s in directors.values(): g.add((s,RDF.type,PC.Director))
  for r in c.execute('SELECT * FROM Movie'):
   fields={'title':r['Title'],'genre':r['Genre']}; name=r['StudioName']
   if name and name.strip():
    s=studio_uri(name); put(g,s,'Studio',{'studioName':name.strip()},src); fields['producedBy']=s
   put(g,PC[f'movie-{r["Id"]}'],'Movie',fields,src)
  for r in c.execute('SELECT * FROM MovieDirector'): g.add((PC[f'movie-{r["MovieId"]}'],PC.directedBy,directors[r['DirectorId']]))
  for r in c.execute('SELECT * FROM PerformanceRole'): put(g,PC[f'role-{r["Id"]}'],'PerformanceRole',{'belongsTo':PC[f'movie-{r["MovieId"]}'],'filledBy':actors[r['ActorId']],'characterName':r['RoleName'],'roleType':r['RoleType']},src)
 finally: c.close()
 return g

def atomic_save(g,path):
 path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix('.tmp'); g.serialize(destination=str(tmp),format='xml'); os.replace(tmp,path)

def initialize(runtime,reset=False):
 MODEL.mkdir(parents=True,exist_ok=True)
 t=ontology(); t.serialize(destination=str(MODEL/'producast.owl'),format='xml')
 from src.dal.catalogue import build_relational,to_rdf
 g=to_rdf(build_relational(ROOT/'data/preprocessed/catalogue.db')); g.serialize(destination=str(MODEL/'seed.rdf'),format='xml')
 if reset or not runtime.exists(): atomic_save(g,runtime)
 return g

class Store:
 def __init__(self,path): self.path=Path(path); self.lock=RLock(); self.schema=ontology()
 def graph(self): return new_graph().parse(self.path,format='xml')
 def select(self,q):
  with self.lock:
   g=self.graph(); return [dict((str(k),v) for k,v in r.asdict().items()) for r in g.query(PREFIX+q)]
 def change(self,fn):
  with self.lock:
   g=self.graph(); result=fn(g); atomic_save(g,self.path); return result
 def all_graph(self):
  with self.lock: return self.schema+self.graph()
