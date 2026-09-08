import concurrent.futures
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
REV='b24c8f5586121d4d2f8a5a793ebac530858dd1ab'
TASKS={'bookreview':[1,2,3],'crmarenapro':[8,12,13],'stockindex':[1,2,3]}
BASE=f'https://raw.githubusercontent.com/ucbepic/DataAgentBench/{REV}/'
def fetch(url):
    with urllib.request.urlopen(url,timeout=120) as r:return r.read()
manifest=fetch(BASE+'dataset_manifest.tsv').decode()
hashes={}
paths=[]
for d,ids in TASKS.items():
    paths += [f'query_{d}/'+p for p in ['db_config.yaml','db_description.txt']]
    paths += [f'query_{d}/query{i}/{p}' for i in ids for p in ['query.json','validate.py','ground_truth.csv']]
for line in manifest.splitlines():
    if any(line.startswith(f'query_{d}/') for d in TASKS):
        p,h,s=line.split('\t'); hashes[p]=(h,int(s));paths.append(p)
def download(p):
    target=ROOT/'upstream'/p
    if target.exists() and (p not in hashes or hashlib.sha256(target.read_bytes()).hexdigest()==hashes[p][0]):return
    data=fetch(BASE+p)
    if data.startswith(b'version https://git-lfs.github.com/spec/v1'):
        data=fetch(f'https://media.githubusercontent.com/media/ucbepic/DataAgentBench/{REV}/{p}')
    if p in hashes:
        h,s=hashes[p]
        assert len(data)==s and hashlib.sha256(data).hexdigest()==h,p
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    print(p,len(data),flush=True)
with concurrent.futures.ThreadPoolExecutor(6) as pool:list(pool.map(download,paths))
(ROOT/'tasks.json').write_text(json.dumps({'commit':REV,'tasks':TASKS,'selection':'Preselected by task text: books, multi-relation CRM metrics, stock time-series analytics; no selection on observed overlap.','hashes':hashes},indent=2)+'\n')
cmd=['docker','exec','-i','dab-bookreview-pg','psql','-X','-v','ON_ERROR_STOP=1','-U','postgres']
exists=subprocess.check_output(cmd+['-d','postgres','-tAc',"SELECT 1 FROM pg_database WHERE datname='crm_support'"],text=True).strip()
if not exists:
    subprocess.run(cmd+['-d','postgres'],input='CREATE DATABASE crm_support;\n',text=True,check=True,capture_output=True)
    sql=(ROOT/'upstream/query_crmarenapro/query_dataset/support.sql').read_text()
    sql+='\nGRANT CONNECT ON DATABASE crm_support TO dab_reader; GRANT USAGE ON SCHEMA public TO dab_reader; GRANT SELECT ON ALL TABLES IN SCHEMA public TO dab_reader; ANALYZE;\n'
    p=subprocess.run(cmd+['-d','crm_support'],input=sql,text=True,capture_output=True)
    (ROOT/'reports/import-crm.log').write_text(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError('CRM import failed; see reports/import-crm.log')
print('Preparation complete',flush=True)
