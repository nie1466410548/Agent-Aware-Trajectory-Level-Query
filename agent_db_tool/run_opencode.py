"""Run one explicitly requested live episode; no automatic retries or grading."""
import argparse
import copy
import json
import os
import signal
import subprocess
import tempfile
import time
from pathlib import Path

from .handler import dump


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    parser.add_argument('--config', required=True, help='Existing OpenCode provider configuration; never copied to the run')
    parser.add_argument('--model', required=True)
    parser.add_argument('--cli', default='opencode')
    parser.add_argument('--timeout', type=int, default=600)
    args = parser.parse_args()
    run = Path(args.run).resolve()
    marker = run / 'live-launch.json'
    if marker.exists():
        raise ValueError('This run already has a live attempt; prepare a new run directory')
    original = json.loads(Path(args.config).read_text())
    provider_name, model_name = args.model.split('/', 1)
    provider = copy.deepcopy(original['provider'][provider_name])
    provider['models'] = {model_name: provider['models'][model_name]}
    config = {'model': args.model, 'small_model': args.model, 'enabled_providers': [provider_name],
              'provider': {provider_name: provider}, 'share': 'disabled', 'autoupdate': False,
              'snapshot': False, 'plugin': [], 'instructions': [],
              'permission': {'*': 'deny', 'agentdb_*': 'allow'},
              'agent': {'trajectory': {'description': 'Analyze with the DB tool.', 'mode': 'primary',
                  'model': args.model, 'prompt': 'Use only agentdb tools. Solve the supplied task independently. Do not delegate. Submit your report with agentdb_submit_answer.',
                  'permission': {'*': 'deny', 'agentdb_*': 'allow'}}},
              'mcp': json.loads((run/'mcp-config.json').read_text())['mcp'],
              'compaction': {'auto': False, 'prune': False}}
    runtime = Path(tempfile.mkdtemp(prefix='agent-db-opencode-'))
    env = {k:v for k,v in os.environ.items() if not k.startswith(('OPENCODE_', 'ANTHROPIC_', 'OPENAI_'))}
    for category in ('config', 'data', 'cache', 'state'):
        path = runtime / category
        path.mkdir()
        env[f'XDG_{category.upper()}_HOME'] = str(path)
    env.update({'OPENCODE_CONFIG_CONTENT': json.dumps(config),
        'OPENCODE_DISABLE_PROJECT_CONFIG':'1', 'OPENCODE_DISABLE_CLAUDE_CODE':'1',
        'OPENCODE_DISABLE_CLAUDE_CODE_PROMPT':'1', 'OPENCODE_DISABLE_CLAUDE_CODE_SKILLS':'1',
        'OPENCODE_DISABLE_AUTOUPDATE':'1', 'OPENCODE_DISABLE_MODELS_FETCH':'1',
        'OPENCODE_EXPERIMENTAL_DISABLE_FILEWATCHER':'1', 'OPENCODE_DISABLE_AUTOCOMPACT':'1',
        'OPENCODE_DISABLE_PRUNE':'1'})
    # Do not serialize provider configuration, API keys, or the environment.
    start = time.time()
    dump(marker, {'model': args.model, 'timeout_s': args.timeout, 'started_at': start,
                  'runtime': str(runtime), 'automatic_task_retries': 0,
                  'provider_retry_policy': 'OpenCode client default'})
    meta = json.loads((run/'task_meta.json').read_text())
    meta['model'] = args.model
    dump(run/'task_meta.json', meta)
    cmd = [args.cli, 'run', '--model', args.model, '--format', 'json', '--pure', '--agent', 'trajectory',
           '--title', 'Agent DB Tool ' + meta['task_id'], (run/'prompt.txt').read_text()]
    timed_out = False
    with (run/'agent.jsonl').open('w') as out, (run/'agent.stderr.log').open('w') as err:
        proc = subprocess.Popen(cmd, cwd=run/'workspace', env=env, stdout=out, stderr=err, start_new_session=True)
        dump(run/'process.json', {'pid': proc.pid, 'started_at': start})
        try:
            proc.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            # Also stop the MCP child if the CLI exited without cleaning it up.
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
    events = [json.loads(s) for s in (run/'events.jsonl').read_text().splitlines()] if (run/'events.jsonl').exists() else []
    requests = [e for e in events if e['record']=='request']
    completions = [e for e in events if e['record']=='completion']
    summary = {'model': args.model, 'exit_code': proc.returncode, 'timed_out': timed_out,
        'duration_s': time.time()-start, 'query_attempts': len(requests),
        'successful_queries': sum(e['response']['status']=='ok' for e in completions),
        'incomplete_requests': len(requests)-len(completions),
        'invalid_hints': sum(bool(e['hint_errors']) for e in requests),
        'provided_hints': sum((e.get('hint_snapshot') or {}).get('status')=='provided' for e in requests),
        'answer_submitted': (run/'answer.md').exists(), 'official_evaluation': 'not_run'}
    dump(run/'summary.json', summary)
    from .report import summarize
    summarize(run)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
