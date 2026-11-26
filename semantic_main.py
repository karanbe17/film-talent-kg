"""Quickstart: python semantic_main.py --reset | --init-only | --queries."""
import argparse
from src.dal.semantic_store import initialize, ROOT, Store
from src.biz.semantic_services import QUERIES
from src.ui.semantic_app import create_app, RUNTIME
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--virtuoso',action='store_true'); p.add_argument('--reset',action='store_true'); p.add_argument('--init-only',action='store_true'); p.add_argument('--queries',action='store_true'); p.add_argument('--port',type=int,default=8000); a=p.parse_args()
 if a.reset or a.init_only or not RUNTIME.exists(): initialize(RUNTIME,a.reset)
 s=Store(RUNTIME)
 if a.virtuoso:
  from src.dal.virtuoso_store import VirtuosoStore
  s=VirtuosoStore(); s.load(a.reset)
 if a.queries:
  for title,q in QUERIES.values():
   print('\n'+title)
   for row in s.select(q):print({k:str(v) for k,v in row.items()})
 elif not a.init_only:
  import uvicorn
  uvicorn.run(create_app(store=s),host='127.0.0.1',port=a.port)
