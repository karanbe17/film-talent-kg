"""Execute standalone DML examples on a scratch graph; no runtime data modified."""
from src.dal.semantic_store import MODEL,new_graph
if __name__=='__main__':
 g=new_graph().parse(MODEL/'seed.rdf',format='xml')
 def run(name,update):
  q=(MODEL/(name+'.sparql')).read_text(); print('\n'+name+'\n'+q)
  if update:g.update(q)
  else:
   rows=list(g.query(q)); print('Results:',rows);return rows
 run('insert_demo',True); assert str(run('select_demo',False)[0][0])=='Temporary Demo'
 run('update_demo',True); assert str(run('select_demo',False)[0][0])=='Updated Demo'
 run('delete_demo',True); assert not run('select_demo',False)
 print('All DML assertions passed; original data unchanged.')
