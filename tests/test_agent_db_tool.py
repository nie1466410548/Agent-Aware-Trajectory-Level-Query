import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from agent_db_tool.dacomp import prepare
from agent_db_tool.handler import Handler
from agent_db_tool.server import Server
from agent_db_tool.validation import validate_hint


def candidate():
    return {'tables': ['sales'], 'columns': ['sales.country', 'sales.amount'], 'priority': 'high', 'likelihood': 'medium'}


def hint():
    return {'status': 'provided', 'coverage': 'partial_plan', 'candidates': [candidate(), candidate()]}


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        upstream = self.root / 'bench/upstream/dacomp-006'
        upstream.mkdir(parents=True)
        db = sqlite3.connect(upstream / 'dacomp-006.sqlite')
        db.executescript("CREATE TABLE sales(country TEXT, amount INTEGER); INSERT INTO sales VALUES ('CA',10),('CA',20),('US',5);")
        db.close()
        (upstream / 'task.json').write_text(json.dumps({'instruction': 'Analyze sales.'}))
        self.run = self.root / 'run'
        prepare('dacomp-006', self.run, self.root / 'bench')
        self.handler = Handler(self.run)

    def tearDown(self):
        self.handler.close()
        self.tmp.cleanup()

    def query(self, future=None, sql='SELECT country, SUM(amount) FROM sales GROUP BY country ORDER BY country', **kw):
        return self.handler.query({'sql': sql, 'future_access': hint() if future is None else future}, **kw)

    def events(self):
        return [json.loads(s) for s in (self.run / 'events.jsonl').read_text().splitlines()]

    def test_actual_sql_multi_candidates_and_archive(self):
        result = self.query()
        self.assertEqual(result['result']['rows'], [['CA', 30], ['US', 5]])
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(self.events()[0]['catalog_check']['status'], 'verified')
        archived = self.handler.read_result(result['result']['result_file'])
        self.assertIn('["CA", 30]', archived['text'])
        self.assertEqual(len(json.loads((self.run/'future_access.json').read_text())['snapshot']['candidates']), 2)

    def test_invalid_hints_clear_old_snapshot_without_reexecution(self):
        self.query()
        for future in [{'status':'provided','coverage':'partial_plan','candidates':[]}, {'garbage':1}]:
            response = self.query(future)
            self.assertEqual(response['status'], 'ok')
            self.assertIsNone(json.loads((self.run/'future_access.json').read_text())['snapshot'])
        response = self.handler.query({'sql':'SELECT 1'})
        self.assertEqual(response['status'], 'ok')
        self.assertEqual(len([e for e in self.events() if e['record']=='completion']), 4)

    def test_empty_statuses_and_no_further_is_not_task_end(self):
        for state in ('unknown', 'no_further_access'):
            self.assertEqual(self.query({'status': state, 'candidates': []})['status'], 'ok')
        self.assertEqual(self.query()['status'], 'ok')

    def test_rejected_execution_does_not_change_snapshot(self):
        self.query()
        snapshot = (self.run/'future_access.json').read_text()
        for args in [{'sql':' '}, {'sql':'SELECT 1','other_sql':'SELECT 2'}, []]:
            self.assertFalse(self.handler.query(args)['sql_executed'])
        self.assertEqual((self.run/'future_access.json').read_text(), snapshot)

    def test_durable_id_replay_and_collision(self):
        first = self.query(request_id='repeat')
        self.handler.close()
        self.handler = Handler(self.run)
        self.assertEqual(self.query(request_id='repeat'), first)
        collision = self.query(sql='SELECT 2', request_id='repeat')
        self.assertFalse(collision['sql_executed'])
        self.assertEqual(len([e for e in self.events() if e['record']=='request']), 1)

    def test_interrupted_request_is_not_reexecuted(self):
        original = self.handler.adapter.execute
        def crash(*unused):
            raise RuntimeError('simulated process failure after request journal')
        self.handler.adapter.execute = crash
        with self.assertRaises(RuntimeError):
            self.query(request_id='inflight')
        self.handler.adapter.execute = original
        self.handler.close()
        self.handler = Handler(self.run)
        self.assertEqual(self.query(request_id='inflight')['status'], 'execution_unknown')
        self.assertFalse(list((self.run/'results').iterdir()))

    def test_write_attach_multistatement_and_sql_error(self):
        for sql in ["DELETE FROM sales", "ATTACH ':memory:' AS other", 'SELECT 1; SELECT 2', 'SELECT missing FROM sales', 'PRAGMA query_only=OFF']:
            self.assertEqual(self.query(sql=sql)['status'], 'db_error')
        self.assertEqual(self.query(sql='SELECT COUNT(*) FROM sales')['result']['rows'], [[3]])

    def test_timeout_and_archive_limit_are_not_success(self):
        self.handler.adapter.timeout = 0.002
        r = self.query(sql='WITH RECURSIVE t(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM t WHERE x<10000000) SELECT SUM(x) FROM t')
        self.assertEqual(r['status'], 'db_error')
        self.handler.adapter.timeout = 120
        self.handler.adapter.result_bytes = 2
        r = self.query()
        self.assertEqual(r['status'], 'db_error')
        self.assertFalse(r['result']['result_complete'])

    def test_read_confinement_and_task_close(self):
        with self.assertRaises(ValueError):
            self.handler.read_result('../task_meta.json')
        self.handler.answer('A supported report.')
        self.assertFalse(self.query()['sql_executed'])
        self.assertIsNone(json.loads((self.run/'future_access.json').read_text())['snapshot'])

    def test_owner_lock(self):
        with self.assertRaises(RuntimeError):
            Handler(self.run)

    def test_semantics_and_limits(self):
        value = hint()
        value['candidates'][0]['filters'] = [{'column':'sales.amount','op':'between','value':[1]}]
        self.assertTrue(validate_hint(value)[1])
        value = hint()
        value['candidates'][0]['aggregations'] = [{'function':'sum','column':'*'}]
        self.assertTrue(validate_hint(value)[1])
        self.assertTrue(validate_hint(hint(), max_candidates=1)[1])
        self.assertTrue(validate_hint(hint(), max_bytes=10)[1])
        self.assertTrue(validate_hint(float('nan'))[1])

    def test_sql_only_backend(self):
        self.handler.close()
        meta = json.loads((self.run/'task_meta.json').read_text())
        meta['mode'] = 'sql-only'
        (self.run/'task_meta.json').write_text(json.dumps(meta))
        self.handler = Handler(self.run)
        self.assertEqual(self.handler.query({'sql':'SELECT 7'})['result']['rows'], [[7]])
        self.assertNotIn('future_access', Server(self.handler).tools()[0]['inputSchema']['properties'])

    def test_native_stdio_protocol(self):
        self.handler.close()
        reqs = [
            {'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'test','version':'1'}}},
            {'jsonrpc':'2.0','method':'notifications/initialized'},
            {'jsonrpc':'2.0','id':2,'method':'tools/list'},
            {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'db_query','arguments':{'sql':'SELECT 42','future_access':{'status':'unknown','candidates':[]}}}},
        ]
        proc = subprocess.run([sys.executable,'-m','agent_db_tool','serve','--run',str(self.run)], input='broken json\n'+'\n'.join(map(json.dumps,reqs))+'\n',text=True,capture_output=True,timeout=10)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        responses = [json.loads(s) for s in proc.stdout.splitlines()]
        self.assertEqual(responses[0]['error']['code'], -32700)
        self.assertEqual(responses[2]['result']['tools'][0]['name'], 'db_query')
        value = json.loads(responses[3]['result']['content'][0]['text'])
        self.assertEqual(value['result']['rows'], [[42]])


if __name__ == '__main__':
    unittest.main()
