"""Import only selected pinned data into dedicated benchmark services."""
import json,subprocess,time
from pathlib import Path
import yaml
from bson import decode_file_iter
from pymongo import MongoClient
ROOT=Path(__file__).resolve().parents[1]
PG=['docker','exec','-i','dab-bookreview-pg','psql','-X','-v','ON_ERROR_STOP=1','-U','postgres']
def main():
 tasks=json.loads((ROOT/'tasks.json').read_text())['tasks'];ready=[]
 for d in tasks:
  root=ROOT/'upstream'/('query_'+d);cfg=root/'db_config.yaml'
  if not cfg.exists():continue
  clients=yaml.safe_load(cfg.read_text())['db_clients'];ok=True
  for name,c in clients.items():
   marker=ROOT/'reports'/f'db-ready-{d}-{name}.json'
   if marker.exists():continue
   typ=c['db_type']
   if typ in ['sqlite','duckdb']:
    path=root/c['db_path']
    if not path.exists():ok=False;continue
    import sqlite3,duckdb
    conn=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True) if typ=='sqlite' else duckdb.connect(str(path),read_only=True)
    conn.execute('SELECT 1');conn.close()
   elif typ=='postgres':
    path=root/c['sql_file']
    if not path.exists():ok=False;continue
    db=c['db_name'];assert db.replace('_','').isalnum()
    exists=subprocess.check_output(PG+['-d','postgres','-tAc',f"SELECT 1 FROM pg_database WHERE datname='{db}'"],text=True).strip()
    if not exists:
     subprocess.run(PG+['-d','postgres','-c',f'CREATE DATABASE "{db}"'],check=True,capture_output=True)
     with path.open('rb') as src,(ROOT/'reports'/f'import-{d}-{name}.log').open('wb') as out:
      subprocess.run(PG+['-d',db],stdin=src,stdout=out,stderr=subprocess.STDOUT,check=True)
    grant=f'GRANT CONNECT ON DATABASE "{db}" TO dab_reader; GRANT USAGE ON SCHEMA public TO dab_reader; GRANT SELECT ON ALL TABLES IN SCHEMA public TO dab_reader;'
    subprocess.run(PG+['-d',db,'-c',grant],capture_output=True,check=True)
   elif typ=='mongo':
    folder=root/c['dump_folder'];files=list(folder.rglob('*.bson'))
    if not files:ok=False;continue
    with MongoClient('mongodb://127.0.0.1:55440',serverSelectionTimeoutMS=10000) as mc:
     db=mc[c['db_name']]
     for file in files:
      coll=db[file.stem]
      if coll.estimated_document_count()==0:
       with file.open('rb') as src:
        batch=[]
        for doc in decode_file_iter(src):
         batch.append(doc)
         if len(batch)==1000:coll.insert_many(batch);batch=[]
        if batch:coll.insert_many(batch)
   else:raise ValueError(typ)
   marker.write_text(json.dumps({'dataset':d,'database':name,'type':typ,'ready_at':time.time()},indent=2)+'\n')
   print('DB READY',d,name,flush=True)
  if ok:
   # Need all task assets before marking dataset ready.
   needed=[root/f'query{i}'/'query.json' for i in tasks[d]]+[root/f'query{i}'/'validate.py' for i in tasks[d]]+[root/'db_description.txt']
   if all(p.exists() for p in needed):ready.append(d)
 (ROOT/'reports/ready-datasets.json').write_text(json.dumps(ready,indent=2)+'\n')
 print('READY DATASETS',ready,flush=True)
if __name__=='__main__':main()
