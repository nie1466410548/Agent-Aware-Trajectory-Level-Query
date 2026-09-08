"""Archive reproducibility checks without calling the benchmark model."""
import hashlib
import json
import platform
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest=json.loads((ROOT/'manifest.json').read_text())
    output={'python':platform.python_version(),'source_revision':manifest['revision'],
            'adapter_files':{p.name:sha(p) for p in sorted((ROOT/'tools').glob('*.py'))},
            'requirements_sha256':sha(ROOT/'requirements-lock.txt'), 'databases':[], 'episodes':[]}
    for task in manifest['tasks']:
        path=ROOT/'upstream'/task['task_id']/(task['task_id']+'.sqlite')
        actual=sha(path)
        output['databases'].append({'task_id':task['task_id'],'sha256':actual,
                                    'matches_pre_run_hash':actual==task['database_sha256']})
    for run in sorted((ROOT/'runs'/'natural').glob('*/*')):
        row={'task_id':run.parent.name,'complete':(run/'run_summary.json').exists(),
             'non_protocol_bash':[], 'reads':[], 'python_access_flags':[], 'result_hash_mismatches':[]}
        for line in (run/'kimi.jsonl').read_text().splitlines():
            event=json.loads(line)
            for call in event.get('tool_calls',[]):
                function=call['function']; args=json.loads(function['arguments'])
                if function['name']=='Bash':
                    command=args.get('command','')
                    prefix=str(ROOT/'.venv'/'bin'/'python')+' '+str(ROOT/'tools'/'tool.py')
                    if not re.fullmatch(re.escape(prefix)+r' (list-db|query-db|python|answer)(?: [^\n;&|`]+)?',command):
                        row['non_protocol_bash'].append(command)
                if function['name']=='Read': row['reads'].append(args)
        calls=[json.loads(l) for l in (run/'tool_calls.jsonl').read_text().splitlines()]
        for c in calls:
            if sha(run/'results'/Path(c['result_file']).name)!=c['result_sha256']:
                row['result_hash_mismatches'].append(c['call_id'])
            if c['tool']=='python':
                flags=re.findall(r'\b(?:sqlite3|read_sql|duckdb|requests|urlopen|subprocess)\b',c.get('code',''))
                if flags: row['python_access_flags'].append({'call_id':c['call_id'],'flags':flags})
        row['note']='Recorded command/source checks only; not an OS security sandbox or formal proof of no unlogged access.'
        output['episodes'].append(row)
    (ROOT/'reports'/'audit.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(output,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
