"""Summarize observed tool behavior; deliberately no prediction-accuracy score."""
import argparse
import json
from collections import Counter
from pathlib import Path

from .handler import dump


def records(path):
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def summarize(run):
    run = Path(run)
    events = records(run/'events.jsonl')
    requests = [e for e in events if e['record']=='request']
    completions = {e['request_id']: e for e in events if e['record']=='completion'}
    calls = records(run/'agent.jsonl')
    usage = [e['part'].get('tokens', {}) for e in calls if e.get('type')=='step_finish']
    steps = []
    for e in requests:
        h = e.get('hint_snapshot') or {}
        cs = h.get('candidates', [])
        steps.append({'step_id':e['step_id'], 'request_id':e['request_id'],
            'hint_status':h.get('status','discarded'), 'candidate_count':len(cs),
            'priorities':[c['priority'] for c in cs], 'likelihoods':[c.get('likelihood') for c in cs],
            'hint_valid':not e['hint_errors'], 'catalog_status':e['catalog_check']['status'],
            'execution_status':completions.get(e['request_id'],{}).get('response',{}).get('status','execution_unknown')})
    result = {'query_attempts':len(requests), 'hint_status_counts':dict(Counter(s['hint_status'] for s in steps)),
        'multi_candidate_calls':sum(s['candidate_count']>1 for s in steps),
        'invalid_hint_calls':sum(not s['hint_valid'] for s in steps),
        'model_steps_with_usage':len(usage),
        'reported_token_sums':{k:sum(u.get(k,0) for u in usage) for k in ('input','output','reasoning','total')},
        'cache_read_tokens':sum(u.get('cache',{}).get('read',0) for u in usage),
        'cache_write_tokens':sum(u.get('cache',{}).get('write',0) for u in usage),
        'token_note':'Provider-reported fields; reasoning/cache accounting may overlap other fields. Not incremental hint cost.',
        'answer_submitted':(run/'answer.md').exists(), 'official_evaluation':'not_run',
        'prediction_accuracy':'not_evaluated', 'steps':steps}
    dump(run/'tool-report.json', result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run',required=True)
    args = parser.parse_args()
    report = summarize(args.run)
    print(json.dumps({k:v for k,v in report.items() if k!='steps'},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
