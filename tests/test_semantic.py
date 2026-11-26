import shutil, tempfile, unittest
from pathlib import Path
from fastapi.testclient import TestClient
from rdflib import RDF, Graph
from src.dal.semantic_store import MODEL, PC, Store, convert, ROOT, ontology
from src.biz.semantic_services import Services, QUERIES
from src.ui.semantic_app import create_app

class SemanticTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.path=Path(self.tmp.name)/'graph.rdf'; shutil.copy(MODEL/'seed.rdf',self.path); self.client=TestClient(create_app(self.path)); self.s=Services(Store(self.path))
 def tearDown(self): self.tmp.cleanup()
 def save(self,k,data):
  r=self.client.post('/'+k+'/save',data=data,follow_redirects=False); self.assertEqual(r.status_code,303); self.assertIn('message=',r.headers['location'],r.headers['location']); return r.headers['location'].split('?')[0].split('/')[-1]
 def test_conversion(self):
  g=convert(ROOT/'data/preprocessed/ProduCast.db'); self.assertEqual(len(set(g.subjects(RDF.type,PC.Person))),13); self.assertEqual(len(set(g.subjects(RDF.type,PC.Movie))),7); self.assertEqual(len(set(g.subjects(RDF.type,PC.PerformanceRole))),6); self.assertIn((PC['person-14'],RDF.type,PC.Actor),g); self.assertIn((PC['person-14'],RDF.type,PC.Director),g)
 def test_pages_and_queries(self):
  for p in ['/', '/movies','/talent','/studios','/awards','/casting','/queries','/explore','/movies/new','/export.rdf','/talent?role=Actor&q=Robert']:
   self.assertEqual(self.client.get(p).status_code,200,p)
  for q in QUERIES:self.assertTrue(self.s.store.select(QUERIES[q][1]),q)
  self.assertIn('Robert Downey Jr.',self.client.get('/talent?role=Actor&q=Robert').text)
  self.assertNotIn('Leonardo DiCaprio',self.client.get('/talent?role=Actor&q=Robert').text)
  self.assertGreater(len(Graph().parse(data=self.client.get('/export.rdf').content,format='xml')),0)
 def test_catalogue_and_producer_profiles(self):
  from src.dal.catalogue import build_relational,to_rdf
  g=to_rdf(build_relational(Path(self.tmp.name)/'catalogue.db'))
  for cls,n in [('Movie',35),('Actor',43),('Director',31),('Award',82),('PerformanceRole',59)]: self.assertEqual(len(set(g.subjects(RDF.type,PC[cls]))),n)
  for a in g.subjects(RDF.type,PC.Actor): self.assertTrue(list(g.subjects(PC.filledBy,a)))
  for d in g.subjects(RDF.type,PC.Director): self.assertTrue(list(g.subjects(PC.directedBy,d)))
  for m in g.subjects(RDF.type,PC.Movie):
   self.assertTrue(list(g.subjects(PC.belongsTo,m)));self.assertTrue(list(g.objects(m,PC.directedBy)));self.assertTrue(list(g.objects(m,PC.producedBy)));self.assertTrue(list(g.objects(m,PC.filmedBy)))
  for a in g.subjects(RDF.type,PC.Award): self.assertTrue(list(g.objects(a,PC.awardedFor)))
  leo=next(r for r in self.s.records('talent') if r['label']=='Leonardo DiCaprio'); page=self.client.get('/talent/'+leo['id']); self.assertEqual(page.status_code,200)
  for term in ['Hugh Glass','Dom Cobb','The Aviator','The Wolf of Wall Street','Academy Award','Golden Globe','Martin Scorsese','Creative collaborators']: self.assertIn(term,page.text)
  self.assertNotIn('SQLite snapshot',page.text); self.assertNotIn('Resource IRI',page.text)
  rocky=next(r for r in self.s.records('movies') if r['label']=='Rocky'); page=self.client.get('/movies/'+rocky['id']);self.assertEqual(page.status_code,200)
  for term in ['John G. Avildsen','Sylvester Stallone','Rocky Balboa','Chartoff-Winkler Productions']: self.assertIn(term,page.text)
  self.assertIn('Martin Scorsese',self.client.get('/explore?repeat=true&q=Leonardo').text)
  self.assertNotIn('Christopher Nolan',self.client.get('/explore?repeat=true&q=Leonardo').text)
  self.assertNotIn('Christopher Nolan',self.client.get('/talent?role=Actor&q=Christopher').text)
  self.assertIn('Christopher Nolan',self.client.get('/talent?role=Director&q=Christopher').text)
 def test_crud_and_persistence(self):
  studio=self.save('studios',{'studioName':'Test Studio','hq':'Victoria'}); actor=self.save('talent',{'name':'Test Person','roles':['Actor','CameraMan']}); director=self.save('talent',{'name':'Test Director','roles':'Director'})
  movie=self.save('movies',{'title':'Test Film','genre':'Drama','producedBy':studio,'directedBy':director,'filmedBy':actor,'duration':'90'})
  role=self.save('casting',{'characterName':'Test Character','roleType':'Lead','filledBy':actor,'belongsTo':movie,'billingOrder':'1'})
  award=self.save('awards',{'awardName':'Test Prize','category':'Camera','year':'2026','receivedBy':actor})
  self.assertEqual(self.s.get('movies',movie)['values']['duration'],'90')
  self.save('movies',{'id':movie,'title':'Updated Film','genre':'Drama','producedBy':studio,'directedBy':director,'filmedBy':actor})
  self.assertEqual(Services(Store(self.path)).get('movies',movie)['label'],'Updated Film')
  # Invalid role type, invalid reference, and in-use studio are rejected.
  r=self.client.post('/casting/save',data={'characterName':'Bad','roleType':'Extra','filledBy':actor,'belongsTo':movie},follow_redirects=False); self.assertIn('error=',r.headers['location'])
  r=self.client.post('/studios/'+studio+'/delete',follow_redirects=False); self.assertIn('error=',r.headers['location'])
  r=self.client.post('/talent/save',data={'id':actor,'name':'Test Person','roles':'CameraMan'},follow_redirects=False); self.assertIn('error=',r.headers['location'])
  self.client.post('/movies/'+movie+'/delete'); self.assertIsNone(self.s.get('movies',movie)); self.assertIsNone(self.s.get('casting',role))
  self.client.post('/talent/'+actor+'/delete'); self.assertIsNone(self.s.get('awards',award))
  self.client.post('/studios/'+studio+'/delete'); self.assertIsNone(self.s.get('studios',studio))
if __name__=='__main__':unittest.main()
