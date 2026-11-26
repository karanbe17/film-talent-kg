"""Exercise the adapter's SPARQL protocol with an in-memory endpoint substitute.
This is not a live Virtuoso integration test. See verify_virtuoso.py for that.
"""
import os, unittest
from unittest.mock import patch
from rdflib import Dataset, URIRef, Literal, RDF
from src.dal.virtuoso_store import VirtuosoStore
from src.dal.semantic_store import PC,MODEL,new_graph
from src.biz.semantic_services import Services, QUERIES

class Response:
 def __init__(self,content=b''):self.content=content
 def raise_for_status(self):pass
 def json(self):
  import json
  return json.loads(self.content)

class ProtocolTests(unittest.TestCase):
 def test_named_graph_roundtrip(self):
  with patch.dict(os.environ,{'PRODUCAST_VIRTUOSO_PASSWORD':'test-only'}):store=VirtuosoStore()
  dataset=Dataset()
  def post(url,data,headers,timeout):
   self.assertTrue(url.endswith('/sparql-auth'))
   q=data['query']; accept=headers['Accept']
   if accept=='text/plain':dataset.update(q);return Response()
   g=dataset.graph(URIRef(data['default-graph-uri'])) if 'default-graph-uri' in data else dataset
   return Response(g.query(q).serialize(format='json' if 'json' in accept else 'xml'))
  with patch.object(store.session,'post',side_effect=post):
   expected=len(new_graph().parse(MODEL/'seed.rdf',format='xml')); schema=len(new_graph().parse(MODEL/'producast.owl',format='xml')); store.load();self.assertEqual(len(store.graph()),expected);self.assertEqual(len(store.all_graph()),expected+schema)
   service=Services(store)
   for _,q in QUERIES.values():store.select(q)
   person=service.save('talent',{'name':['Protocol Test'],'roles':['Actor']})
   self.assertEqual(service.get('talent',person)['label'],'Protocol Test')
   service.save('talent',{'name':['Updated'],'roles':['Actor']},person)
   self.assertEqual(service.get('talent',person)['label'],'Updated')
   service.delete('talent',person);self.assertIsNone(service.get('talent',person))
   store.load();self.assertEqual(len(store.graph()),expected)
