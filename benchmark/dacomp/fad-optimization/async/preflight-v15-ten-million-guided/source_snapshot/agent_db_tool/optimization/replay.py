"""Isolated replay worker. The controller never receives this stream or its path."""
import argparse
import hashlib
import json
import os
import platform
import resource
import shutil
import sqlite3
import tempfile
import time
from pathlib import Path

from .backend import TaskBackend
from .controller import Controller
from .patterns import receive

DEFAULT_CONFIG = {
    'version': 'sqlite-fad-v1.5-budgeted-multiple-builds', 'min_fad_occurrences': 2,
    'max_index_match_fraction': 0.1,
    'max_index_objects': 2, 'max_materialization_objects': 12,
    'max_extra_bytes': 512 * 1024 * 1024, 'build_seconds': 120,
    'optimizer_seconds': 300, 'query_seconds': 120,
    'absolute_tolerance': 1e-7, 'relative_tolerance': 1e-9,
    'cache_mode': 'full-base-read-then-new-connection',
    'preparation_outside_timer': ['copy', 'prewarm', 'input/config hashes', 'result directory'],
}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for data in iter(lambda: f.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def io_stats():
    try:
        return {k: int(v) for k, v in (line.split(':') for line in Path('/proc/self/io').read_text().splitlines())}
    except OSError:
        return {}


def worker(database, events, out, mode, config, diagnostic=False):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    (out / 'results').mkdir()
    manifest = {'database_sha256': sha(database), 'events_sha256': sha(events),
                'config': config, 'mode': mode, 'diagnostic': diagnostic,
                'pid': os.getpid(), 'sqlite': sqlite3.sqlite_version,
                'python': platform.python_version(), 'affinity': sorted(os.sched_getaffinity(0)),
                'load_before': os.getloadavg(), 'cache_mode': config['cache_mode']}
    with tempfile.TemporaryDirectory(prefix='fad-replay-') as scratch:
        copied = Path(scratch) / 'task.sqlite'
        prep = time.perf_counter()
        shutil.copyfile(database, copied)
        # Benchmark input extraction is preparation. The baseline DB receives
        # SQL-only requests, never FAD values or their serialized bytes.
        requests = Path(scratch) / 'requests.jsonl'
        with Path(events).open() as source, requests.open('w') as dest:
            for line in source:
                event = json.loads(line)
                if event.get('record') != 'request':
                    continue
                args = {'sql': event['arguments']['sql']}
                if mode != 'baseline':
                    args['future_access'] = event['arguments'].get('future_access')
                dest.write(json.dumps({'record': 'request', 'step_id': event['step_id'], 'arguments': args}, ensure_ascii=False) + '\n')
        manifest['database_input'] = 'sql_only' if mode == 'baseline' else 'sql_and_fad'
        manifest['request_input_sha256'] = sha(requests)
        warm = TaskBackend(copied, config['query_seconds'])
        warm.prewarm()
        warm.close()
        manifest['preparation_seconds'] = time.perf_counter() - prep
        io_before, cpu_before = io_stats(), time.process_time()
        start = time.perf_counter()
        backend = TaskBackend(copied, config['query_seconds'])
        controller = None if mode == 'baseline' else Controller(backend, mode, config)
        records, peak_extra = [], 0
        with requests.open() as stream, (out / 'events.jsonl').open('w') as log:
            for line in stream:
                event = json.loads(line)
                if event.get('record') != 'request':
                    continue
                step, args = event['step_id'], event['arguments']
                before_objects = [o['name'] for o in controller.objects] if controller else []
                if controller is None:
                    executed, used, rejections = args['sql'], [], []
                    rewrite_seconds = 0.0
                else:
                    before = time.perf_counter()
                    original_plan = backend.explain(args['sql'])
                    if original_plan and original_plan[0][0] == 'error':
                        executed, used, rejections = args['sql'], [], ['original SQL fails preparation; preserve original statement']
                    else:
                        executed, used, rejections = controller.rewrite(args['sql'])
                    rewrite_seconds = time.perf_counter() - before
                # Diagnostic plans run only in the separate correctness cohort.
                plan = backend.explain(executed) if diagnostic else None
                result = backend.execute(executed, out / 'results' / f'Q{step}.jsonl')
                if controller is None:
                    fad, audit, decisions = None, {'status': 'not_received'}, []
                    receive_seconds = decision_seconds = 0.0
                    extra = 0
                else:
                    before = time.perf_counter()
                    fad, audit = receive(args.get('future_access'), backend.catalog)
                    receive_seconds = time.perf_counter() - before
                    before = time.perf_counter()
                    decisions = controller.observe_fad(step, fad)
                    decision_seconds = time.perf_counter() - before
                    extra = backend.space()
                peak_extra = max(peak_extra, extra)
                record = {'step': step, 'sql': args['sql'], 'executed_sql': executed,
                          'raw_fad': args.get('future_access'), 'fad': fad, 'fad_audit': audit,
                          'available_before_query': before_objects, 'materializations_used': used,
                          'rewrite_rejections': rejections, 'plan': plan,
                          'receive_seconds': receive_seconds, 'rewrite_seconds': rewrite_seconds,
                          'decision_including_build_seconds': decision_seconds,
                          'actions': decisions, 'extra_allocated_bytes': extra, **result}
                log.write(json.dumps(record, ensure_ascii=False) + '\n')
                records.append(record)
        cleanup_seconds = controller.cleanup() if controller else 0.0
        backend.close()
        total = time.perf_counter() - start
        cpu = time.process_time() - cpu_before
        io_after = io_stats()
        summary = {'total_seconds': total, 'query_seconds': sum(r['query_seconds'] for r in records),
                   'fad_receive_seconds': sum(r['receive_seconds'] for r in records),
                   'rewrite_seconds': sum(r['rewrite_seconds'] for r in records),
                   'decision_including_build_seconds': sum(r['decision_including_build_seconds'] for r in records),
                   'build_including_estimate_seconds': sum(a.get('build_seconds', 0) for r in records for a in r['actions']),
                   'cleanup_seconds': cleanup_seconds, 'cpu_seconds': cpu,
                   'peak_rss_kib_process_including_prewarm': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                   'io_delta': {k: io_after[k] - io_before.get(k, 0) for k in io_after},
                   'peak_extra_allocated_bytes': peak_extra, 'sql_attempts': len(records),
                   'sql_successes': sum(r['status'] == 'ok' for r in records),
                   'rewritten_queries': [r['step'] for r in records if r['materializations_used']],
                   'objects': controller.objects if controller else [], 'manifest': manifest}
        components = sum(summary[k] for k in ('query_seconds', 'fad_receive_seconds', 'rewrite_seconds',
                                            'decision_including_build_seconds', 'cleanup_seconds'))
        summary['common_setup_logging_close_seconds'] = total - components
        (out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', required=True)
    parser.add_argument('--events', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--mode', choices=('baseline', 'index', 'materialization', 'combined'), required=True)
    parser.add_argument('--config')
    parser.add_argument('--diagnostic', action='store_true')
    args = parser.parse_args()
    config = json.loads(Path(args.config).read_text()) if args.config else DEFAULT_CONFIG
    summary = worker(args.database, args.events, args.out, args.mode, config, args.diagnostic)
    print(json.dumps({k: summary[k] for k in ('total_seconds', 'sql_attempts', 'sql_successes', 'rewritten_queries')}))


if __name__ == '__main__':
    main()
