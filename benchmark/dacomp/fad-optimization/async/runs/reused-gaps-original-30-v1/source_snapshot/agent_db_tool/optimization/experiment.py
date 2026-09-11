"""Serial randomized AB/BA runner; freezes source/config before formal measurement."""
import argparse
import json
import os
import platform
import random
import shutil
import subprocess
import sys
from pathlib import Path

from .check import compare_runs
from .replay import DEFAULT_CONFIG, sha

MODES = ('index', 'materialization', 'combined')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', required=True)
    parser.add_argument('--events', required=True)
    parser.add_argument('--root', required=True)
    parser.add_argument('--pairs', type=int, default=20)
    parser.add_argument('--seed', type=int, default=20260910)
    parser.add_argument('--validation-root', required=True)
    args = parser.parse_args()
    if args.pairs < 1:
        parser.error('pairs must be positive')
    root = Path(args.root).resolve()
    root.mkdir(parents=True, exist_ok=False)
    frozen = root / 'source_snapshot'
    frozen.mkdir()
    source_paths = sorted(Path('agent_db_tool/optimization').glob('*.py')) + [Path('agent_db_tool/v02.py'), Path('agent_db_tool/sqlite_adapter.py')]
    hashes = {}
    for p in source_paths:
        hashes[str(p)] = sha(p)
        dest = frozen / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, dest)
    config = root / 'config.json'
    config.write_text(json.dumps(DEFAULT_CONFIG, indent=2) + '\n')
    for mode in MODES:
        check = compare_runs(Path(args.validation_root) / 'baseline', Path(args.validation_root) / mode, DEFAULT_CONFIG)
        if not check['all_equal']:
            raise RuntimeError('correctness precondition failed: ' + mode)
    affinity = sorted(os.sched_getaffinity(0))
    # Pin all workers to the same available logical CPU; do not claim exclusive use.
    os.sched_setaffinity(0, {affinity[0]})
    manifest = {'database': str(Path(args.database).resolve()), 'database_sha256': sha(args.database),
                'events': str(Path(args.events).resolve()), 'events_sha256': sha(args.events),
                'source_hashes': hashes, 'pairs_per_mode': args.pairs, 'seed': args.seed,
                'platform': platform.platform(), 'cpuinfo': Path('/proc/cpuinfo').read_text().split('\n\n')[0],
                'meminfo': Path('/proc/meminfo').read_text(), 'pinned_cpu': affinity[0],
                'original_cpu_affinity': affinity, 'validation_root': args.validation_root,
                'disk': shutil.disk_usage(root)._asdict(),
                'dependencies': subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True)}
    rng = random.Random(args.seed)
    jobs = [(m, n) for m in MODES for n in range(1, args.pairs + 1)]
    rng.shuffle(jobs)
    order = []
    for mode, repeat in jobs:
        arms = ['baseline', mode]
        rng.shuffle(arms)
        order.append({'mode': mode, 'repeat': repeat, 'arms': arms})
    manifest['execution_order'] = order
    (root / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    for number, job in enumerate(order, 1):
        mode, repeat = job['mode'], job['repeat']
        pair = root / mode / f'pair-{repeat:02d}'
        for arm in job['arms']:
            out = pair / arm
            cmd = [sys.executable, '-m', 'agent_db_tool.optimization.replay', '--database', args.database,
                   '--events', args.events, '--config', str(config), '--out', str(out), '--mode', arm]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if out.exists():
                (out / 'worker-output.txt').write_text(result.stdout + result.stderr)
            if result.returncode:
                raise RuntimeError(f'worker failed: {out}: {result.stderr}')
        checks = compare_runs(pair / 'baseline', pair / mode, DEFAULT_CONFIG)
        (pair / 'correctness.json').write_text(json.dumps(checks, indent=2) + '\n')
        if not checks['all_equal']:
            raise RuntimeError(f'formal correctness failure retained at {pair}')
        print(f'{number}/{len(order)} pairs complete: {mode} {repeat}; all results equal', flush=True)
    for p, expected in hashes.items():
        if sha(p) != expected:
            raise RuntimeError('source changed during formal experiment: ' + p)
    if sha(args.database) != manifest['database_sha256'] or sha(args.events) != manifest['events_sha256']:
        raise RuntimeError('source database or trajectory changed')
    (root / 'COMPLETE.json').write_text(json.dumps({'pairs': len(order), 'all_equal': True}) + '\n')


if __name__ == '__main__':
    main()
