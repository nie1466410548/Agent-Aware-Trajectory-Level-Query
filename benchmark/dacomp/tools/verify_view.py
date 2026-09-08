"""Replay a manually selected filtered or aggregate view outside agent logs.

This verifies answer coverage on this database, not performance or an online
predictor. Build timing and plan selection are not benchmarked here.
"""
import argparse
import json
import math
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    candidate = json.loads(args.candidate.read_text())
    task = candidate['task_id']
    inv = json.loads((ROOT/'reports'/f'{task}-pilot-01-inventory.json').read_text())
    queries = {q['id']:q for q in inv['queries']}
    database = ROOT/'upstream'/task/f'{task}.sqlite'
    # Main database remains read-only. Only TEMP storage is written.
    db = sqlite3.connect(database.resolve().as_uri()+'?mode=ro',uri=True)
    db.execute('CREATE TEMP TABLE reuse_candidate AS '+candidate['build_sql'])
    rows = db.execute('SELECT COUNT(*) FROM reuse_candidate').fetchone()[0]
    checks=[]
    for qid in candidate['covered_queries']:
        q=queries[qid]
        original=q['sql']
        if qid in candidate.get('rewritten_queries', {}):
            replacement = candidate['rewritten_queries'][qid]
        else:
            replacement, n = re.subn(r'\bFROM\s+"?sheet1"?\b', 'FROM reuse_candidate', original, flags=re.I)
            if n != 1:
                raise ValueError('Expected exactly one sheet1 FROM for '+qid)
        cursor=db.execute(replacement)
        columns=[d[0] for d in cursor.description]
        result=cursor.fetchall()
        archived_path=ROOT/'runs'/'natural'/task/inv['summary']['run_id']/'results'/(q['call_id']+'-rows.json')
        archived=json.loads(archived_path.read_text())
        # Compare multisets to avoid treating unspecified row order as semantics.
        normalize=lambda rs:sorted(json.dumps(list(row),ensure_ascii=False) for row in rs)
        check={'query_id':qid,'rewritten_sql':replacement,'row_count':len(result),
                       'columns_match':columns==archived['columns'],
                       'rows_match_exactly':normalize(result)==normalize(archived['rows'])}
        keys=candidate.get('comparison_keys',{}).get(qid)
        if keys:
            positions=[columns.index(k) for k in keys]
            key=lambda row:tuple(row[i] for i in positions)
            a,b=sorted(result,key=key),sorted(archived['rows'],key=key)
            assert len({key(row) for row in a})==len(a), 'Comparison keys must be unique'
            differences=[]
            def equal(x,y):
                if isinstance(x,(int,float)) and isinstance(y,(int,float)):
                    differences.append(abs(x-y))
                    return math.isclose(x,y,rel_tol=1e-12,abs_tol=1e-9)
                return x==y
            check['rows_match_numeric_tolerance']=len(a)==len(b) and all(all(equal(x,y) for x,y in zip(ra,rb)) for ra,rb in zip(a,b))
            check['numeric_tolerance']={'relative':1e-12,'absolute':1e-9}
            check['max_absolute_numeric_difference']=max(differences,default=0)
        checks.append(check)
    output={**candidate,'view_rows':rows,'checks':checks,
            'all_results_equal':all(c['columns_match'] and c['rows_match_exactly'] for c in checks),
            'all_results_match_exactly_or_with_declared_tolerance':all(c['columns_match'] and (c['rows_match_exactly'] or c.get('rows_match_numeric_tolerance',False)) for c in checks),
            'interpretation':'Offline selected candidate; future queries were known to the analyst. No latency benefit or online frontier prediction demonstrated.'}
    out=ROOT/'reports'/(args.candidate.stem+'-verification.json')
    out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(output,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
