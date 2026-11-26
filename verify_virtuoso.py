"""Live verification against a disposable named graph; never touches the app graph."""
from uuid import uuid4
from src.dal.virtuoso_store import VirtuosoStore
from src.biz.semantic_services import Services,QUERIES
from src.dal.semantic_store import MODEL,new_graph
if __name__=='__main__':
 s=VirtuosoStore('https://github.com/karanbe17/film-talent-kg/graph/test-'+uuid4().hex)
 try:
  s.load(); expected=len(new_graph().parse(MODEL/'seed.rdf',format='xml')); assert len(s.graph())==expected; assert len(s.all_graph())==expected+len(new_graph().parse(MODEL/'producast.owl',format='xml'))
  for title,q in QUERIES.values():print(title, len(s.select(q)), 'rows')
  a=Services(s); key=a.save('talent',{'name':['Virtuoso verification'],'roles':['Actor']})
  assert a.get('talent',key)['label']=='Virtuoso verification'
  a.save('talent',{'name':['Updated verification'],'roles':['Actor']},key)
  assert a.get('talent',key)['label']=='Updated verification'
  a.delete('talent',key);assert a.get('talent',key) is None
  print('Live Virtuoso SELECT, INSERT, UPDATE, DELETE and graph loading passed.')
 finally:
  for iri in [s.data,s.schema]:s.update(f'CLEAR SILENT GRAPH {iri.n3()}')
