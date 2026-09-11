"""Online controller: its only workload input is the current, already-arrived FAD."""
import sqlite3
import time
from collections import defaultdict

from .backend import quote
from .patterns import digest, index_patterns, material_pattern
from .rewrite import material_select, rewrite, preserve_rounding_scan_order


class Controller:
    def __init__(self, backend, mode, config):
        self.backend, self.mode, self.config = backend, mode, config
        self.objects, self.attempted = [], set()
        self.seen = defaultdict(list)
        self.optimizer_seconds = 0.0
        self.budget = min(backend.database.stat().st_size, config['max_extra_bytes'])
        self.latest = None
        with backend.trusted() as db:
            self.rows = {t: db.execute('SELECT COUNT(*) FROM ' + quote(t)).fetchone()[0]
                         for t in backend.catalog}
            self.originally_unindexed = {t for t in backend.catalog if not db.execute('PRAGMA index_list(' + quote(t) + ')').fetchall()}
            self.initial_schema = db.execute("SELECT type, name, sql FROM sqlite_master ORDER BY name").fetchall()

    def propose_actions(self, fad):
        actions = {}
        for i, candidate in enumerate((fad or {}).get('candidates', [])):
            priority = {'high': 0, 'medium': 1, 'low': 2}[candidate['priority']]
            patterns = []
            if self.mode in ('index', 'combined'):
                patterns += [('index', p) for p in index_patterns(candidate)]
            if self.mode in ('materialization', 'combined'):
                try:
                    patterns.append(('materialization', material_pattern(candidate)))
                except ValueError:
                    pass
            for kind, pattern in patterns:
                key = digest([kind, pattern])
                action = {'key': key, 'kind': kind, 'pattern': pattern,
                          'priority': priority, 'candidate_indices': [i + 1]}
                if key in actions:
                    actions[key]['priority'] = min(actions[key]['priority'], priority)
                    actions[key]['candidate_indices'].append(i + 1)
                else:
                    actions[key] = action
        return list(actions.values())

    def estimate(self, action):
        p = action['pattern']
        if action['kind'] == 'index':
            expressions = p['keys']
            from_sql = ' FROM ' + quote(p['table'])
            count = self.rows[p['table']]
        else:
            select, _ = material_select(p)
            expressions = [f'g{i}' for i in range(len(p['groups']))]
            expressions += [f'a{i}' for i in range(len(p['aggregations']))]
            from_sql = ' FROM (' + select + ')'
            count = None
        width = ' + '.join('COALESCE(length(CAST((' + e + ') AS BLOB)),0)' for e in expressions) or '0'
        # This conservative width/group count scan is real optimization work, timed.
        row = self.backend.db.execute('SELECT COUNT(*), MAX(' + width + ')' + from_sql).fetchone()
        count = row[0] if count is None else count
        return int((count + 1) * ((row[1] or 0) + 32 + len(expressions) * 12) * 2 + 8192)

    def build(self, action, step):
        start = time.perf_counter()
        obj = dict(action, name='fad_' + action['kind'][0] + '_' + action['key'],
                   created_after=step, source_steps=list(self.seen[action['key']]))
        if action['kind'] == 'index':
            obj['ddl'] = 'CREATE INDEX ' + quote(obj['name']) + ' ON ' + quote(obj['pattern']['table']) + '(' + ', '.join(obj['pattern']['keys']) + ')'
        else:
            select, obj['replacements'] = material_select(obj['pattern'])
            if obj['pattern']['table'] in self.originally_unindexed:
                table_sql = ' FROM ' + quote(obj['pattern']['table'])
                select = select.replace(table_sql, table_sql + ' NOT INDEXED', 1)
            obj['ddl'] = 'CREATE TEMP TABLE ' + quote(obj['name']) + ' AS ' + select
        before = self.backend.space()
        try:
            with self.backend.trusted() as db:
                remaining = max(0, self.budget - before)
                main_pages = db.execute('PRAGMA main.page_count').fetchone()[0]
                temp_pages = db.execute('PRAGMA temp.page_count').fetchone()[0]
                schema = 'main' if action['kind'] == 'index' else 'temp'
                pages = main_pages if schema == 'main' else temp_pages
                limit = pages + remaining // self.backend.page_size
                db.execute(f'PRAGMA {schema}.max_page_count={max(pages, limit)}')
                deadline = start + min(self.config['build_seconds'],
                                       max(0, self.config['optimizer_seconds'] - self.optimizer_seconds))
                db.set_progress_handler(lambda: int(time.perf_counter() > deadline), 1000)
                obj['estimated_bytes'] = self.estimate(action)
                if obj['estimated_bytes'] > remaining:
                    raise ValueError('conservative size estimate exceeds remaining budget')
                db.execute(obj['ddl'])
            after = self.backend.space()
            obj['allocated_bytes'] = max(0, after - before)
            if after > self.budget:
                raise ValueError('space budget exceeded')
            obj['status'] = 'built'
            self.objects.append(obj)
        except (sqlite3.Error, ValueError) as exc:
            obj['status'], obj['error'] = 'rejected_or_failed', str(exc)
            with self.backend.trusted() as db:
                db.execute('DROP ' + ('INDEX' if action['kind'] == 'index' else 'TABLE') + ' IF EXISTS ' + quote(obj['name']))
        obj['build_seconds'] = time.perf_counter() - start
        return obj

    def observe_fad(self, step, fad):
        start = time.perf_counter()
        self.latest = fad
        actions = self.propose_actions(fad)
        decisions = []
        for a in actions:
            self.seen[a['key']].append(step)
        actions.sort(key=lambda a: (a['priority'], -len(self.seen[a['key']]), a['key']))
        built = False
        for a in actions:
            key, kind = a['key'], a['kind']
            reason = None
            if key in self.attempted:
                reason = 'already built or attempted'
            elif len(self.seen[key]) < self.config['min_fad_occurrences']:
                reason = 'waiting for second FAD occurrence'
            elif sum(o['kind'] == kind for o in self.objects) >= self.config['max_' + kind + '_objects']:
                reason = 'object count budget reached; keep existing objects until task end'
            elif built:
                reason = 'one build attempt per step'
            elif self.optimizer_seconds + time.perf_counter() - start >= self.config['optimizer_seconds']:
                reason = 'optimizer time budget reached'
            if reason:
                decisions.append(dict(a, status='skipped', reason=reason, source_steps=list(self.seen[key])))
                continue
            self.attempted.add(key)
            built = True
            decisions.append(self.build(a, step))
        self.optimizer_seconds += time.perf_counter() - start
        return decisions

    def rewrite(self, sql):
        start = time.perf_counter()
        executed, used, reasons = rewrite(sql, self.objects, self.backend.catalog)
        if any(o['kind'] == 'index' for o in self.objects):
            executed, guarded = preserve_rounding_scan_order(executed, self.originally_unindexed)
            if guarded:
                reasons.append('ROUND with aggregation: preserve original full scan with NOT INDEXED')
        result = executed, used, reasons
        self.optimizer_seconds += time.perf_counter() - start
        return result

    def cleanup(self):
        start = time.perf_counter()
        with self.backend.trusted() as db:
            for obj in reversed(self.objects):
                db.execute('DROP ' + ('INDEX' if obj['kind'] == 'index' else 'TABLE') + ' ' + quote(obj['name']))
        return time.perf_counter() - start
