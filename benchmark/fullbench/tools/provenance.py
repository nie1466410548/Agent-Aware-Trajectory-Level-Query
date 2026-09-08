"""Additional completed-trace review flags, including commands that also invoke adapters."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 flags=[];messages_checked=0;scripts_checked=0
 for report in sorted((ROOT/'reports').glob('*-*-full-01.json')):
  summary=json.loads(report.read_text());run=ROOT/'runs'/summary['group']/summary['task_id']/'full-01'
  stream=run/'kimi.jsonl'
  if not stream.exists():continue
  def inspect(text,source,index,kind):
   reasons=[]
   if re.search(r'\b(?:psycopg2|sqlite3|duckdb|pymongo)\b|\b(?:MongoClient|read_sql|psql|mongosh)\b',text):reasons.append('possible_direct_database_access_review')
   if str(ROOT/'upstream') in text:reasons.append('upstream_path_in_tool_arguments_review')
   if any(word in text for word in ['ground_truth.csv','validate.py','kimi-code/config','credentials.json']):reasons.append('evaluation_or_configuration_path_review')
   for path in re.findall(r'/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/[^\s\'"<>;]+',text):
    if '/.venv/' in path or str(ROOT/'tools/tool.py') in path:continue
    if path.startswith(str(run)+'/') or path==str(run):continue
    reasons.append('path_outside_assigned_run_review');break
   if reasons:
    flags.append({'task':summary['task_id'],'group':summary['group'],'source':source,'index':index,'kind':kind,'reasons':sorted(set(reasons)),'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'text':text})
  for index,line in enumerate(stream.read_text().splitlines()):
   try:m=json.loads(line)
   except ValueError:continue
   if m.get('role')!='assistant':continue
   messages_checked+=1
   for tc in m.get('tool_calls',[]):
    fn=tc.get('function',{})
    try:arguments=json.loads(fn.get('arguments','{}'))
    except (ValueError,TypeError):continue
    inspect(json.dumps(arguments,ensure_ascii=False),str(stream.relative_to(ROOT)),index,fn.get('name'))
  for file in (run/'results').glob('*.py'):
   scripts_checked+=1;inspect(file.read_text(),str(file.relative_to(ROOT)),None,'saved_python')
 out={'completed_reports_checked':len(list((ROOT/'reports').glob('*-*-full-01.json'))),'assistant_messages_checked':messages_checked,'saved_scripts_checked':scripts_checked,'flags':flags,'interpretation':'Flags need context review; a path/import match alone is not proof of leakage or direct DB access.'}
 (ROOT/'reports/provenance-review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('Checked messages',messages_checked,'saved Python',scripts_checked,'flags',len(flags))
 for f in flags:print(f['task'],f['group'],f['index'],f['reasons'])
if __name__=='__main__':main()
