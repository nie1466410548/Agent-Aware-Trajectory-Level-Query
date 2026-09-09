"""Fixed-revision streaming data preparation; no model calls."""
import csv, json, sqlite3, time, urllib.request
from common import *
BASE = f'https://huggingface.co/datasets/DAComp/dacomp-da/resolve/{REVISION}'
def fetch(remote, path):
    tmp = path.with_suffix(path.suffix+'.part'); path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(BASE+'/'+remote, timeout=120) as r, tmp.open('wb') as w:
        expected=r.headers.get('Content-Length'); size=0
        while b:=r.read(1024*1024): w.write(b); size+=len(b)
        if expected is not None and size!=int(expected): raise IOError(f'Truncated download: {size}/{expected}')
    tmp.replace(path)
def main():
    source=ROOT/'manifests/dacomp-da.jsonl'
    if not source.exists(): fetch('dacomp-da.jsonl',source)
    tasks=records(source); ids=[t['instance_id'] for t in tasks]
    assert len(ids)==100 and set(ids)=={f'dacomp-{i:03}' for i in range(1,101)}
    dump(ROOT/'manifests/source.json',{'revision':REVISION,'sha256':sha(source),'count':100})
    previous={t['task_id']:t for t in records(ROOT/'manifests/tasks.jsonl')}
    rows=[]
    for task in sorted(tasks,key=lambda t:t['instance_id']):
        tid=task['instance_id']; p=BENCH/'upstream'/tid/f'{tid}.sqlite'
        row={'task_id':tid,'task':task,'revision':REVISION,'database_path':str(p),'phase':'preparation'}
        try:
            if not p.exists(): fetch(f'{tid}/{tid}.sqlite',p)
            digest=sha(p)
            if previous.get(tid,{}).get('database_sha256')==digest and previous[tid].get('status')=='ready': row=previous[tid]
            else:
                db=sqlite3.connect(p.resolve().as_uri()+'?mode=ro',uri=True)
                check=db.execute('PRAGMA quick_check').fetchall(); assert check==[('ok',)],check
                tables=[]
                for name,ddl in db.execute("SELECT name,sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall():
                    quoted='"'+name.replace('"','""')+'"'
                    info=db.execute('PRAGMA table_info('+quoted+')').fetchall()
                    tables.append({'name':name,'ddl':ddl,'rows':db.execute('SELECT COUNT(*) FROM '+quoted).fetchone()[0], 'columns':[{'name':r[1],'type':r[2]} for r in info]})
                db.close(); row.update(status='ready',database_sha256=digest,database_bytes=p.stat().st_size,tables=tables,quick_check='ok')
        except Exception as e: row.update(status='preparation_failed',error=repr(e))
        rows.append(row)
        # Persist all tasks, including pending ones, at each checkpoint.
        allrows=rows+[previous.get(t['instance_id'],{'task_id':t['instance_id'],'task':t,'revision':REVISION,'status':'not_prepared'}) for t in sorted(tasks,key=lambda x:x['instance_id']) if t['instance_id'] not in {r['task_id'] for r in rows}]
        target=ROOT/'manifests/tasks.jsonl'; tmp=target.with_suffix('.part'); tmp.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in allrows)); tmp.replace(target)
        print(tid,row['status'],row.get('database_bytes'),len(row.get('tables',[])),flush=True)
    with (ROOT/'manifests/databases.csv').open('w') as f:
        w=csv.writer(f); w.writerow(['task_id','status','bytes','sha256','table','rows','columns'])
        for r in rows:
            for t in r.get('tables',[{}]): w.writerow([r['task_id'],r['status'],r.get('database_bytes'),r.get('database_sha256'),t.get('name'),t.get('rows'),json.dumps(t.get('columns'),ensure_ascii=False)])
    ready=[r for r in rows if r['status']=='ready']
    multi=next(r['task_id'] for r in ready if len(r['tables'])>1 and r['task_id'] not in ['dacomp-005','dacomp-061'])
    order=['dacomp-005',multi,'dacomp-061']+[r['task_id'] for r in rows if r['task_id'] not in ['dacomp-005',multi,'dacomp-061']]
    queue=ROOT/'state/queue.json'
    if not queue.exists(): dump(queue,{'batch':BATCH,'acceptance_tasks':order[:3],'order':order,'tasks':{r['task_id']:{'status':'pending' if r['status']=='ready' else r['status']} for r in rows}})
if __name__=='__main__': main()
