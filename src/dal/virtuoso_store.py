"""Virtuoso HTTP SPARQL adapter. RDFLib is used for conversion and validation only."""
import os
from threading import RLock
import requests
from requests.auth import HTTPDigestAuth
from rdflib import URIRef, Literal, BNode
from .semantic_store import PREFIX, new_graph, MODEL

class VirtuosoStore:
 def __init__(self, graph_iri=None):
  self.base=os.environ.get('PRODUCAST_VIRTUOSO_URL','http://127.0.0.1:8890').rstrip('/')
  self.data=URIRef(graph_iri or 'https://github.com/karanbe17/film-talent-kg/graph/data')
  self.schema=URIRef(str(self.data)+'/ontology')
  self.session=requests.Session()
  self.session.auth=HTTPDigestAuth(os.environ.get('PRODUCAST_VIRTUOSO_USER','dba'),os.environ['PRODUCAST_VIRTUOSO_PASSWORD'])
  self.lock=RLock()
 def request(self,query,accept,graph=None):
  params={'query':query}
  if graph is not None: params['default-graph-uri']=str(graph)
  r=self.session.post(self.base+'/sparql-auth',data=params,headers={'Accept':accept},timeout=45)
  r.raise_for_status(); return r
 def update(self,q):
  self.request(q,'text/plain')
 def select(self,q):
  with self.lock:
   result=self.request(PREFIX+q,'application/sparql-results+json',self.data).json()
   def term(v):
    if v['type']=='uri': return URIRef(v['value'])
    if v['type']=='bnode': return BNode(v['value'])
    return Literal(v['value'],lang=v.get('xml:lang'),datatype=v.get('datatype'),normalize=False)
   return [{k:term(v) for k,v in row.items()} for row in result['results']['bindings']]
 def read_graph(self,iri):
  r=self.request(f'CONSTRUCT {{ ?s ?p ?o }} WHERE {{ GRAPH {iri.n3()} {{ ?s ?p ?o }} }}','application/rdf+xml')
  return new_graph().parse(data=r.content,format='xml')
 def graph(self): return self.read_graph(self.data)
 def all_graph(self):
  with self.lock:return self.read_graph(self.schema)+self.graph()
 @staticmethod
 def triples(g):return '\n'.join(f'{s.n3()} {p.n3()} {o.n3()} .' for s,p,o in g)
 def load(self,reset=False):
  with self.lock:
   for iri,name in [(self.schema,'producast.owl'),(self.data,'seed.rdf')]:
    if not reset and len(self.read_graph(iri)):continue
    g=new_graph().parse(MODEL/name,format='xml')
    self.update(f'CLEAR SILENT GRAPH {iri.n3()}')
    lines=self.triples(g).splitlines()
    step=len(lines) if any(isinstance(t,BNode) for triple in g for t in triple) else 100
    for i in range(0,len(lines),max(1,step)):
     block='\n'.join(lines[i:i+step]); self.update(f'INSERT DATA {{ GRAPH {iri.n3()} {{ {block} }} }}')
 def change(self,fn):
  with self.lock:
   before=self.graph(); after=new_graph(); after+=before
   result=fn(after); removed=before-after; added=after-before
   # The instance graph contains named resources only. Send a single scoped SPARQL update.
   if removed or added:
    q=[]
    if removed:q.append(f'DELETE DATA {{ GRAPH {self.data.n3()} {{ {self.triples(removed)} }} }}')
    if added:q.append(f'INSERT DATA {{ GRAPH {self.data.n3()} {{ {self.triples(added)} }} }}')
    self.update(';\n'.join(q))
   return result
