"""Enumerate final continuation opportunities without reselecting verified cases."""
import json
from common import *
from opportunities import enumerate_candidates

def main():
 auth=json.loads((ROOT/'state/recovery-authorization.json').read_text());profiles=records(REPORT/'sql_profile.jsonl')
 for tid in auth['resume_tasks']:
  path=REPORT/'tasks'/f'{tid}.analysis.json'
  if not path.exists():continue
  old=json.loads(path.read_text());queries=[q for q in profiles if q['task_id']==tid and q['category']=='data' and q['status']=='success']
  def key(c):return json.dumps({k:c.get(k) for k in ['type','build_sql','covered','rewrites']},sort_keys=True)
  candidates=old['candidates'];known={key(c) for c in candidates};index=max([int(c['candidate_id'][1:]) for c in candidates],default=0)
  for candidate in enumerate_candidates(queries):
   if key(candidate) in known:continue
   index+=1;candidate.update(candidate_id=f'C{index}',status='not_verified_cap',cost_conclusion='Final continuation candidate enumerated only; original per-task three-case verification selection retained.')
   candidates.append(candidate);known.add(key(candidate))
  old.update(candidates=candidates,fingerprint=sha(ROOT/'runs'/BATCH/tid/'attempt-01/sql_events.jsonl'),continuation_analysis_scope='All final SQL enumerated; original verification selections and IDs preserved, added candidates explicitly unverified.')
  dump(path,old);print(tid,len(candidates),'final candidates')
if __name__=='__main__':main()
