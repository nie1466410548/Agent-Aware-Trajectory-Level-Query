"""Audit completed episode coverage and source/result integrity without executing queries."""
import hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(4*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def main():
 manifest=json.loads((ROOT/'tasks.json').read_text());issues=[];episodes=[]
 for ds,ids in manifest['tasks'].items():
  for i in ids:
   for group in ['natural','fad']:
    report=ROOT/'reports'/f'{group}-{ds}-query{i}-full-01.json'
    if not report.exists():continue
    run=ROOT/'runs'/group/ds/f'query{i}'/'full-01'
    summary=json.loads(report.read_text());events=[json.loads(line) for line in (run/'tool_calls.jsonl').read_text().splitlines()] if (run/'tool_calls.jsonl').exists() else []
    meta=json.loads((run/'task_meta.json').read_text())
    for key,value in {'task_id':f'{ds}/query{i}','group':group,'run_id':'full-01','upstream_commit':manifest['commit'],'hints':False}.items():
     if meta.get(key)!=value:issues.append({'run':str(run.relative_to(ROOT)),'issue':'episode metadata mismatch','key':key})
    if summary.get('task_id')!=meta['task_id'] or summary.get('group')!=group:issues.append({'run':str(run.relative_to(ROOT)),'issue':'validation report identity mismatch'})
    checked=0;statements=0
    for e in events:
     files=[]
     if e.get('result_sha256'):files.append((e['result_file'],e['result_sha256']))
     for st in e.get('statement_results',[]):files.append((st['result_file'],st['result_sha256']));statements+=1
     for filename,digest in files:
      p=Path(filename)
      if not p.exists() or sha(p)!=digest:issues.append({'run':str(run.relative_to(ROOT)),'file':filename,'issue':'result hash mismatch/missing'})
      checked+=1
    sqls=[e for e in events if isinstance(e.get('sql'),str)]
    mongos=[e for e in events if 'mongo_request' in e or e.get('dialect')=='mongo']
    if (run/'analysis.json').exists():
     for n,e in enumerate(sqls,1):
      p=run/'sql'/f"{n:03d}-{e['call_id']}.sql"
      if not p.exists() or p.read_text().strip()!=e['sql'].strip():issues.append({'run':str(run.relative_to(ROOT)),'issue':'SQL export mismatch','call':e['call_id']})
     for n,e in enumerate(mongos,1):
      p=run/'mongo'/f"{n:03d}-{e['call_id']}.json"
      if not p.exists() or json.loads(p.read_text())!=e.get('mongo_request',{'operation':'unknown'}):issues.append({'run':str(run.relative_to(ROOT)),'issue':'Mongo export mismatch','call':e['call_id']})
    else:issues.append({'run':str(run.relative_to(ROOT)),'issue':'analysis missing'})
    process=json.loads((run/'process.json').read_text())
    try:os.kill(process['pid'],0);issues.append({'run':str(run.relative_to(ROOT)),'issue':'completed report but process PID still alive (verify PID reuse)'})
    except ProcessLookupError:pass
    episodes.append({'task':f'{ds}/query{i}','group':group,'sql_calls':len(sqls),'mongo_calls':len(mongos),'adapter_version':meta.get('adapter_version'),'statement_result_files':statements,'checked_result_hashes':checked,'passed':summary['validator_passed']})
 expected=2*sum(map(len,manifest['tasks'].values()))
 result={'expected_episodes':expected,'completed_episodes':len(episodes),'all_episodes_finished':len(episodes)==expected,'episodes':episodes,'issues':issues}
 (ROOT/'reports/artifact-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print('Audit',len(episodes),'/',expected,'issues',len(issues),'hashes',sum(x['checked_result_hashes'] for x in episodes))
if __name__=='__main__':main()
