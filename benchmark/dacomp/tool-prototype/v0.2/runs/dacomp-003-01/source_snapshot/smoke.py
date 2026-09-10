"""Deterministic DAComp integration checks; no model or forecasting claims."""
import argparse
import json
import sqlite3
from pathlib import Path

from .dacomp import prepare
from .handler import Handler, dump


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--benchmark', default=str(Path(__file__).resolve().parents[1]/'benchmark/dacomp'))
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    results = []
    for task in ('dacomp-006','dacomp-003','dacomp-004','dacomp-005'):
        run = output/task
        meta = prepare(task, run, args.benchmark)
        table = next(iter(meta['catalog']))
        col = meta['catalog'][table][0]
        quoted = '"' + table.replace('"','""') + '"'
        sql = f'SELECT COUNT(*) AS n FROM {quoted}'
        db = sqlite3.connect(Path(meta['database_path']).as_uri()+'?mode=ro', uri=True)
        expected = db.execute(sql).fetchone()[0]
        db.close()
        handler = Handler(run)
        try:
            future = {'status':'provided','coverage':'partial_plan','candidates':[
                {'tables':[table],'columns':[f'{table}.{col}'],'priority':'high','likelihood':'medium'},
                {'tables':[table],'priority':'high','likelihood':'medium'}]}
            response = handler.query({'sql':sql,'future_access':future})
            assert response['status']=='ok' and response['result']['rows']==[[expected]]
            invalid = handler.query({'sql':'SELECT 1','future_access':{'broken':True}})
            assert invalid['status']=='ok'
            assert json.loads((run/'future_access.json').read_text())['snapshot'] is None
            for state in ('unknown','no_further_access'):
                assert handler.query({'sql':'SELECT 1','future_access':{'status':state,'candidates':[]}})['status']=='ok'
            handler.answer('Deterministic integration check only; no Agent analysis or official grading.')
        finally:
            handler.close()
        results.append({'task':task,'database_sha256':meta['database_sha256'], 'table':table,
                        'expected_count':expected,'passed':True,'model_calls':0})
    dump(output/'report.json', {'kind':'deterministic_tool_integration','results':results})
    print(json.dumps(results, indent=2))


if __name__=='__main__':
    main()
