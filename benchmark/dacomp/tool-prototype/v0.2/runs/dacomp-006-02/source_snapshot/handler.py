"""One process owns one trajectory; journal before executing, never auto-retry."""
import fcntl
import json
import os
import time
import uuid
from pathlib import Path

from .sqlite_adapter import SQLiteAdapter
from .validation import catalog_check, execution_errors, validate_hint


def dump(path, value):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')
    os.replace(temp, path)


class Handler:
    def __init__(self, run):
        self.run = Path(run).resolve()
        self.meta = json.loads((self.run / 'task_meta.json').read_text())
        self.lock = (self.run / 'owner.lock').open('a')
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.lock.close()
            raise RuntimeError('Another process owns this trajectory')
        self.hints = self.meta.get('mode', 'hints') == 'hints'
        self.version = self.meta.get('schema_version', '0.1')
        self.max_candidates = self.meta.get('max_candidates', 8)
        self.adapter = SQLiteAdapter(self.meta['database_path'],
            timeout=self.meta.get('sql_timeout_s', 120), result_bytes=self.meta.get('result_limit_bytes', 16*1024*1024))
        self.catalog = self.meta.get('catalog', {})
        self.journal = self.run / 'events.jsonl'
        events = [json.loads(line) for line in self.journal.read_text().splitlines()] if self.journal.exists() else []
        self.requests = {e['request_id']: e for e in events if e['record'] == 'request'}
        self.responses = {e['request_id']: e['response'] for e in events if e['record'] == 'completion'}
        self.step = max([e['step_id'] for e in self.requests.values()] + [0])
        self.closed = (self.run / 'answer.md').exists()
        (self.run / 'results').mkdir(exist_ok=True)
        # A new process does not inherit an unconfirmed in-flight prediction.
        dump(self.run / 'future_access.json', {'snapshot': None, 'reason': 'process_start'})

    def record(self, event):
        with self.journal.open('a', encoding='utf-8') as out:
            out.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + '\n')
            out.flush()
            os.fsync(out.fileno())

    def query(self, args, request_id=None):
        request_id = request_id or uuid.uuid4().hex
        # Never use caller-provided IDs as filesystem paths.
        if not isinstance(request_id, str) or not request_id:
            return {'status': 'invalid_arguments', 'sql_executed': False, 'errors': [{'path': 'request_id', 'message': 'Expected a nonempty string'}]}
        if request_id in self.requests:
            if args != self.requests[request_id]['arguments']:
                return {'request_id': request_id, 'status': 'invalid_arguments', 'sql_executed': False,
                        'errors': [{'path': 'request_id', 'message': 'Request ID reused with different arguments'}]}
            return self.responses.get(request_id, {'request_id': request_id, 'status': 'execution_unknown', 'sql_executed': None})
        errors = execution_errors(args, self.hints)
        if errors or self.closed or self.step >= self.meta.get('query_attempt_limit', 80):
            return {'request_id': request_id, 'status': 'invalid_arguments', 'sql_executed': False,
                    'errors': errors or [{'path': '', 'message': 'Task closed or query limit reached'}]}
        validation_start = time.perf_counter()
        if self.hints and self.version == '0.2':
            from .v02 import validate
            hint, hint_errors, checked = validate(args.get('future_access'), self.catalog, self.max_candidates)
        else:
            hint, hint_errors = validate_hint(args.get('future_access'), self.max_candidates) if self.hints else (None, [])
            checked = catalog_check(hint, self.catalog)
        self.step += 1
        event = {'record': 'request', 'schema_version': self.version, 'trajectory_id': self.meta['trajectory_id'],
                 'step_id': self.step, 'request_id': request_id, 'time': time.time(), 'arguments': args,
                 'hint_snapshot': hint, 'hint_errors': hint_errors, 'catalog_check': checked,
                 'hint_validation_ms': (time.perf_counter()-validation_start)*1000}
        self.record(event)
        self.requests[request_id] = event
        dump(self.run / 'future_access.json', {'request_id': request_id, 'step_id': self.step, 'snapshot': hint})
        archive = self.run / 'results' / f'{self.step:04d}.rows.jsonl'
        result = self.adapter.execute(args['sql'], archive)
        internal = {'engine_statements': result.pop('engine_statements'), 'duration_ms': result.pop('duration_ms')}
        response = {'request_id': request_id, **result}
        self.record({'record': 'completion', 'request_id': request_id, 'step_id': self.step,
                     'time': time.time(), 'response': response, **internal})
        self.responses[request_id] = response
        return response

    def read_result(self, path, offset=0, limit=16000):
        if not isinstance(path, str) or type(offset) is not int or type(limit) is not int or offset < 0 or not 1 <= limit <= 30000:
            raise ValueError('Expected result path, nonnegative offset and limit in 1..30000')
        target = (self.run / path).resolve()
        if not target.is_relative_to((self.run / 'results').resolve()) or not target.is_file():
            raise ValueError('Only existing result archives may be read')
        # Byte offsets; avoid splitting UTF-8 by returning a base64-free decoded chunk
        # with the stream cookie as the next offset.
        with target.open(encoding='utf-8') as stream:
            stream.seek(offset)
            text = stream.read(limit)
            next_offset = stream.tell()
        return {'text': text, 'next_offset': next_offset, 'eof': next_offset >= target.stat().st_size}

    def answer(self, markdown):
        if not isinstance(markdown, str) or not markdown.strip():
            raise ValueError('Nonempty Markdown report required')
        if self.closed:
            raise ValueError('Task already closed')
        (self.run / 'answer.md').write_text(markdown, encoding='utf-8')
        self.closed = True
        dump(self.run / 'future_access.json', {'snapshot': None, 'reason': 'task_completed'})
        self.record({'record': 'task_completed', 'time': time.time(), 'official_evaluation': 'not_run'})
        return {'submitted': True, 'official_evaluation': 'not_run'}

    def close(self):
        if not self.lock.closed:
            fcntl.flock(self.lock, fcntl.LOCK_UN)
            self.lock.close()
