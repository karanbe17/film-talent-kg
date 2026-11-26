"""Curated demonstration catalogue, separate from the historical SQLite snapshot."""
from pathlib import Path
from hashlib import sha256
import sqlite3
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[2]
RAW=ROOT/'data/raw'

def key(prefix,label): return prefix+'-'+sha256(label.encode('utf-8')).hexdigest()[:18]
def rows(name):
 for line in (RAW/name).read_text(encoding='utf-8').splitlines():
  if line.strip(): yield line.split('|')

def build_relational(path):
 """Build a new normalized relational staging database; never overwrite Milestone 4."""
 path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists(): path.unlink()
 with sqlite3.connect(path) as c:
  c.executescript('''PRAGMA foreign_keys=ON;
  CREATE TABLE Person(id TEXT PRIMARY KEY,name TEXT NOT NULL);
  CREATE TABLE Profession(person_id TEXT REFERENCES Person(id),role TEXT,PRIMARY KEY(person_id,role));
  CREATE TABLE Studio(id TEXT PRIMARY KEY,name TEXT NOT NULL);
  CREATE TABLE Movie(id TEXT PRIMARY KEY,title TEXT NOT NULL,release_year INTEGER NOT NULL,genre TEXT,studio_id TEXT NOT NULL REFERENCES Studio(id),source_url TEXT);
  CREATE TABLE MovieDirector(movie_id TEXT REFERENCES Movie(id),person_id TEXT REFERENCES Person(id),PRIMARY KEY(movie_id,person_id));
  CREATE TABLE MovieCamera(movie_id TEXT REFERENCES Movie(id),person_id TEXT REFERENCES Person(id),PRIMARY KEY(movie_id,person_id));
  CREATE TABLE PerformanceRole(id TEXT PRIMARY KEY,movie_id TEXT REFERENCES Movie(id),actor_id TEXT REFERENCES Person(id),character_name TEXT NOT NULL);
  CREATE TABLE Award(id TEXT PRIMARY KEY,person_id TEXT REFERENCES Person(id),movie_id TEXT REFERENCES Movie(id),award_name TEXT,category TEXT,year INTEGER,source_url TEXT);
  ''')
  def person(name,role):
   k=key('person',name); c.execute('INSERT OR IGNORE INTO Person VALUES (?,?)',(k,name)); c.execute('INSERT OR IGNORE INTO Profession VALUES (?,?)',(k,role)); return k
  films={}; people={}
  for title,year,genre,studio,dirs,camera,cast in rows('film_catalogue.txt'):
   mid=key('movie',title+'|'+year); sid=key('studio',studio); films[title]=mid
   c.execute('INSERT OR IGNORE INTO Studio VALUES (?,?)',(sid,studio))
   source='https://www.imdb.com/find/?q='+quote(title+' '+year)
   c.execute('INSERT INTO Movie VALUES (?,?,?,?,?,?)',(mid,title,int(year),genre,sid,source))
   for name in dirs.split(';'):
    pid=person(name,'Director'); people[name]=pid; c.execute('INSERT INTO MovieDirector VALUES (?,?)',(mid,pid))
   for name in camera.split(';'):
    pid=person(name,'CameraMan'); people[name]=pid; c.execute('INSERT INTO MovieCamera VALUES (?,?)',(mid,pid))
   for credit in cast.split(';'):
    name,character=credit.split('~'); pid=person(name,'Actor'); people[name]=pid
    c.execute('INSERT INTO PerformanceRole VALUES (?,?,?,?)',(key('role',mid+pid+character),mid,pid,character))
  for name,film,year,award,category in rows('award_catalogue.txt'):
   source=f'https://www.oscars.org/oscars/ceremonies/{year}' if award=='Academy Award' else 'https://goldenglobes.com/winners-nominees/'
   c.execute('INSERT INTO Award VALUES (?,?,?,?,?,?,?)',(key('award',name+film+year+award+category),people[name],films[film],award,category,int(year),source))
  assert not c.execute('PRAGMA foreign_key_check').fetchall()
 return path

def to_rdf(path):
 from src.dal.semantic_store import new_graph,PC,put
 g=new_graph(); source='Curated Milestone 5 film catalogue (selected credits and wins)'
 with sqlite3.connect(path) as c:
  for k,name in c.execute('SELECT * FROM Person'): put(g,PC[k],'Person',{'name':name},source)
  from rdflib import RDF
  for k,role in c.execute('SELECT * FROM Profession'): g.add((PC[k],RDF.type,PC[role]))
  for k,name in c.execute('SELECT * FROM Studio'): put(g,PC[k],'Studio',{'studioName':name},source)
  for k,title,y,genre,sid,url in c.execute('SELECT * FROM Movie'): put(g,PC[k],'Movie',{'title':title,'releaseYear':str(y),'genre':genre,'producedBy':PC[sid],'referenceUrl':url},source)
  for table,p in [('MovieDirector','directedBy'),('MovieCamera','filmedBy')]:
   for mid,pid in c.execute('SELECT * FROM '+table): g.add((PC[mid],PC[p],PC[pid]))
  for k,mid,pid,char in c.execute('SELECT * FROM PerformanceRole'): put(g,PC[k],'PerformanceRole',{'belongsTo':PC[mid],'filledBy':PC[pid],'characterName':char},source)
  for k,pid,mid,name,cat,y,url in c.execute('SELECT * FROM Award'): put(g,PC[k],'Award',{'receivedBy':PC[pid],'awardedFor':PC[mid],'awardName':name,'category':cat,'year':str(y),'referenceUrl':url},source)
 return g
