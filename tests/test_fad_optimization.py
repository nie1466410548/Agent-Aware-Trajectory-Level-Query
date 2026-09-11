"""Correctness/isolation tests for the experimental persistent replay backend."""
import copy
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

HAS_DEPS = importlib.util.find_spec('sqlglot') is not None and importlib.util.find_spec('jsonschema') is not None
if HAS_DEPS:
    from agent_db_tool.optimization.backend import TaskBackend
    from agent_db_tool.optimization.controller import Controller
    from agent_db_tool.optimization.patterns import receive
    from agent_db_tool.optimization.replay import DEFAULT_CONFIG
    from agent_db_tool.optimization.rewrite import rewrite, preserve_rounding_scan_order
    from agent_db_tool.optimization.check import compare_results


def prediction(groups=True, functions=('sum',)):
    field = lambda state, items: {'status': state, 'items': items}
    return {'status': 'provided', 'coverage': 'partial_plan', 'candidates': [{
        'tables': ['sales'], 'priority': 'high',
        'columns': field('known', ['sales.amount']),
        'filters': field('none', []), 'joins': field('none', []),
        'group_by': field('known' if groups else 'none', [{'type': 'column', 'column': 'sales.category'}] if groups else []),
        'aggregations': field('known', [{'function': f, 'column': 'sales.amount'} for f in functions])}]}


@unittest.skipUnless(HAS_DEPS, 'requires optimization requirements')
class OptimizationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name)
        db = sqlite3.connect(self.path / 'base.sqlite')
        db.execute('CREATE TABLE sales(category TEXT, amount REAL)')
        db.executemany('INSERT INTO sales VALUES (?,?)', [('a', 1), ('a', None), ('b', 3), ('b', 3), ('c', None)])
        db.commit()
        db.close()
        self.backend = TaskBackend(self.path / 'base.sqlite')
        self.config = dict(DEFAULT_CONFIG)
        # The tiny fixture needs more than its initial two pages to materialize.
        self.backend.database = self.path / 'budget-file'
        self.backend.database.write_bytes(b'0' * 1024 * 1024)

    def tearDown(self):
        self.backend.close()
        self.tmp.cleanup()

    def build(self, fad=None, mode='materialization'):
        c = Controller(self.backend, mode, self.config)
        hint, audit = receive(fad or prediction(), self.backend.catalog)
        self.assertFalse(audit['errors'])
        c.observe_fad(1, hint)
        self.assertEqual(c.objects, [])
        c.observe_fad(2, hint)
        self.assertEqual(len(c.objects), 1)
        return c

    def assert_same(self, sql, controller):
        changed, used, _ = controller.rewrite(sql)
        a = self.backend.db.execute(sql)
        ac, ar = [x[0] for x in a.description], a.fetchall()
        b = self.backend.db.execute(changed)
        bc, br = [x[0] for x in b.description], b.fetchall()
        self.assertTrue(compare_results(ar, br, ac, bc, False)['equal'], (sql, changed, ar, br))
        return used

    def test_sql_only_baseline_never_invokes_fad_or_optimizer(self):
        from unittest.mock import patch
        from agent_db_tool.optimization.replay import worker
        events = self.path / 'requests.jsonl'
        events.write_text(json.dumps({'record': 'request', 'step_id': 1, 'arguments': {
            'sql': 'SELECT COUNT(*) AS n FROM sales', 'future_access': 'deliberately invalid FAD'}}) + '\n')
        with patch('agent_db_tool.optimization.replay.receive', side_effect=AssertionError('FAD called')), \
             patch('agent_db_tool.optimization.replay.Controller', side_effect=AssertionError('optimizer created')), \
             patch.object(TaskBackend, 'explain', side_effect=AssertionError('extra planning')), \
             patch.object(TaskBackend, 'space', side_effect=AssertionError('optimization accounting')):
            result = worker(self.path / 'base.sqlite', events, self.path / 'baseline', 'baseline', self.config)
        self.assertEqual(result['sql_successes'], 1)
        self.assertEqual(result['manifest']['database_input'], 'sql_only')
        for key in ('fad_receive_seconds', 'rewrite_seconds', 'decision_including_build_seconds', 'cleanup_seconds'):
            self.assertEqual(result[key], 0)
        record = json.loads((self.path / 'baseline/events.jsonl').read_text())
        self.assertIsNone(record['raw_fad'])
        self.assertIsNone(record['fad'])

    def test_readonly_restored_after_ddl(self):
        c = self.build()
        for sql in ('DELETE FROM sales', 'DROP TABLE sales', 'PRAGMA query_only=OFF', "ATTACH ':memory:' AS other", 'CREATE TEMP TABLE attack(x)', 'BEGIN'):
            self.assertEqual(self.backend.execute(sql, self.path / 'result')['status'], 'error', sql)
        self.assert_same('SELECT category, SUM(amount) AS s FROM sales GROUP BY category', c)
        c.cleanup()
        self.assertEqual(self.backend.db.execute('SELECT COUNT(*) FROM sales').fetchone()[0], 5)

    def test_nulls_duplicates_and_multiple_aggregates(self):
        c = self.build(prediction(functions=('sum', 'count', 'min', 'max', 'avg')))
        self.assertTrue(self.assert_same('SELECT category, SUM(amount) AS s, COUNT(amount) AS n, MIN(amount) AS lo, MAX(amount) AS hi, AVG(amount) AS a FROM sales GROUP BY category', c))

    def test_global_empty_aggregate(self):
        with self.backend.trusted() as db:
            db.execute('DELETE FROM sales')
        c = self.build(prediction(groups=False, functions=('sum', 'count', 'avg')))
        self.assertTrue(self.assert_same('SELECT SUM(amount) AS s, COUNT(amount) AS n, AVG(amount) AS a FROM sales', c))
        self.assertFalse(c.rewrite('SELECT 1 AS x FROM sales')[1])

    def test_nested_aliases(self):
        c = self.build()
        self.assertTrue(self.assert_same('SELECT SUM(s) AS total FROM (SELECT category AS cat, SUM(amount) AS s FROM sales GROUP BY cat)', c))
        self.assertTrue(self.assert_same('SELECT category, ROUND(SUM(amount), 2) AS s FROM sales GROUP BY 1 ORDER BY s', c))

    def test_cte_leaf_materialization_preserves_outer_calculation(self):
        c = self.build()
        sql = ('WITH monthly AS (SELECT category AS m, SUM(amount) AS p FROM sales GROUP BY 1), '
               'totals AS (SELECT SUM(p) AS total FROM monthly) '
               'SELECT m, p, ROUND(p / NULLIF(total,0),3) AS share FROM monthly CROSS JOIN totals ORDER BY m')
        self.assertTrue(self.assert_same(sql, c))
        self.assertTrue(self.assert_same('WITH x(k,v) AS (SELECT category, SUM(amount) AS s FROM sales GROUP BY category) SELECT k,v FROM x ORDER BY k', c))

    def test_cte_shadowed_base_name_is_not_rewritten(self):
        c = self.build()
        sql = ('WITH sales AS (SELECT category, amount * 10 AS amount FROM main.sales) '
               'SELECT category, SUM(amount) AS s FROM sales GROUP BY category')
        self.assertFalse(self.assert_same(sql, c))
        recursive = 'WITH RECURSIVE x(n) AS (VALUES(1) UNION ALL SELECT n+1 FROM x WHERE n<3) SELECT category,SUM(amount) AS s FROM sales GROUP BY category'
        self.assertEqual(c.rewrite(recursive)[0], recursive)

    def test_index_admission_counts_actual_leading_filter(self):
        with self.backend.trusted() as db:
            db.execute('DELETE FROM sales')
            db.executemany('INSERT INTO sales VALUES (?,?)', [('common',1)]*99+[('rare',2)])
        for value,expected in [('common',False),('rare',True)]:
            fad=prediction()
            fad['candidates'][0]['aggregations']={'status':'none','items':[]}
            fad['candidates'][0]['filters']={'status':'known','items':[{
                'type':'predicate','column':'sales.category','op':'eq','value':{'status':'known','literal':value}}]}
            hint,_=receive(fad,self.backend.catalog)
            c=Controller(self.backend,'index',self.config)
            c.observe_fad(1,hint);actions=c.observe_fad(2,hint)
            assessment=actions[0]['index_assessment']
            self.assertEqual(assessment['matched_rows'],99 if value=='common' else 1)
            self.assertEqual(assessment['accepted'],expected)
            self.assertEqual(bool(c.objects),expected)
            c.cleanup()
        detail=prediction();detail['candidates'][0]['aggregations']={'status':'none','items':[]}
        hint,_=receive(detail,self.backend.catalog)
        c=Controller(self.backend,'index',self.config)
        c.observe_fad(1,hint);actions=c.observe_fad(2,hint)
        self.assertFalse(c.objects)
        self.assertEqual(actions[0]['status'],'rejected_by_cost_gate')

    def test_new_metrics_extend_family_without_future_inference(self):
        self.config['max_materialization_objects']=1
        c=self.build(prediction(functions=('sum',)))
        first=copy.deepcopy(c.objects[0])
        sql='SELECT category,SUM(amount) AS s,COUNT(amount) AS n FROM sales GROUP BY category'
        self.assertFalse(self.assert_same(sql,c))
        c.observe_fad(3,receive(prediction(functions=('count',)),self.backend.catalog)[0])
        self.assertEqual(len(c.objects),2)
        self.assertEqual(c.objects[0],first)
        self.assertEqual(c.objects[-1]['source_steps'],[1,2,3])
        self.assertTrue(self.assert_same(sql,c))
        self.assertEqual(c.objects[0],first)

    def test_aggregate_build_uses_single_pass_and_precompiled_rules(self):
        from unittest.mock import patch
        with patch.object(Controller,'estimate',side_effect=AssertionError('duplicate aggregate scan')):
            c=self.build()
        before=copy.deepcopy(c.objects)
        with patch('agent_db_tool.optimization.rewrite.prepare_matcher',side_effect=AssertionError('foreground recompilation')):
            self.assertTrue(self.assert_same('SELECT category,SUM(amount) AS s FROM sales GROUP BY category',c))
        self.assertEqual(c.objects,before)

    def test_single_pass_space_cap_rejects_large_group_output(self):
        with self.backend.trusted() as db:
            db.executemany('INSERT INTO sales VALUES (?,?)',[(str(i)+'x'*100,1) for i in range(2000)])
            self.backend.base_pages=db.execute('PRAGMA page_count').fetchone()[0]
        c=Controller(self.backend,'materialization',self.config);c.budget=self.backend.page_size
        fad=receive(prediction(),self.backend.catalog)[0]
        c.observe_fad(1,fad);actions=c.observe_fad(2,fad)
        self.assertEqual(actions[0]['status'],'rejected_or_failed')
        self.assertFalse(c.objects)
        self.assertEqual(self.backend.db.execute('SELECT COUNT(*) FROM sales').fetchone()[0],2005)
        self.assertEqual(self.backend.execute('DELETE FROM sales',self.path/'r')['status'],'error')

    def test_noncovering_index_guard_respects_cte_scope(self):
        from agent_db_tool.optimization.rewrite import reject_noncovering_fad_scan
        sql='WITH totals AS (SELECT category,SUM(amount) AS s FROM sales GROUP BY category) SELECT * FROM totals'
        rewritten,changed=reject_noncovering_fad_scan(sql,[[0,0,0,'SEARCH sales USING INDEX fad_i_test']],{'sales'})
        self.assertTrue(changed);self.assertIn('NOT INDEXED',rewritten)
        self.assertEqual(self.backend.db.execute(sql).fetchall(),self.backend.db.execute(rewritten).fetchall())
        self.assertFalse(reject_noncovering_fad_scan(sql,[[0,0,0,'SEARCH sales USING COVERING INDEX fad_i_test']],{'sales'})[1])
        shadow='WITH sales AS (SELECT 1 AS amount) SELECT * FROM sales'
        self.assertFalse(reject_noncovering_fad_scan(shadow,[[0,0,0,'SEARCH sales USING INDEX fad_i_test']],{'sales'})[1])

    def test_unsupported_queries_fall_back(self):
        c = self.build()
        for sql in (
            "SELECT category, SUM(amount) AS s FROM sales WHERE category='a' GROUP BY category",
            'SELECT category, AVG(amount) AS s FROM sales GROUP BY category',
            'SELECT category, COUNT(DISTINCT amount) AS s FROM sales GROUP BY category',
            'SELECT category, SUM(other.amount) AS s FROM sales GROUP BY category',
            'WITH sales AS (SELECT 1 AS amount, 2 AS category) SELECT category, SUM(amount) AS s FROM sales GROUP BY category',
            'SELECT category, SUM(amount) AS s FROM sales GROUP BY category HAVING s>2',
            'SELECT category, RANDOM() AS r, SUM(amount) AS s FROM sales GROUP BY category',
            'SELECT SUM(amount) AS s FROM sales',
        ):
            self.assertEqual(c.rewrite(sql)[0], sql, sql)

    def test_order_alias_wins_over_same_named_base_column(self):
        c = self.build()
        self.assertTrue(self.assert_same('SELECT category AS c, SUM(amount) AS category FROM sales GROUP BY c ORDER BY category DESC', c))

    def test_unknown_filter_not_guessed(self):
        fad = prediction()
        fad['candidates'][0]['filters'] = {'status': 'partial', 'items': [{'type': 'predicate', 'column': 'sales.category', 'op': 'eq', 'value': {'status': 'unknown'}}]}
        hint, audit = receive(fad, self.backend.catalog)
        self.assertFalse(audit['errors'])
        c = Controller(self.backend, 'materialization', self.config)
        for step in range(1, 4):
            c.observe_fad(step, hint)
        self.assertEqual(c.objects, [])

    def test_decode_one_layer_and_union_no_inference(self):
        hint, audit = receive(json.dumps(prediction()), self.backend.catalog)
        self.assertTrue(audit['decoded_string'])
        self.assertIn('sales.category', hint['candidates'][0]['columns']['items'])
        self.assertEqual(hint['candidates'][0]['filters']['status'], 'none')
        self.assertIsNone(receive(json.dumps(json.dumps(prediction())), self.backend.catalog)[0])

    def test_one_occurrence_per_round_and_no_rebuild(self):
        fad = prediction()
        fad['candidates'].append(copy.deepcopy(fad['candidates'][0]))
        c = self.build(fad)
        c.observe_fad(3, receive(fad, self.backend.catalog)[0])
        self.assertEqual(len(c.objects), 1)
        self.assertEqual(c.objects[0]['source_steps'], [1, 2])
        c.observe_fad(4, {'status': 'no_further_access', 'candidates': []})
        self.assertEqual(len(c.objects), 1)

    def test_space_failure_leaves_queries_working(self):
        c = Controller(self.backend, 'materialization', self.config)
        c.budget = 1
        fad = receive(prediction(), self.backend.catalog)[0]
        c.observe_fad(1, fad)
        actions = c.observe_fad(2, fad)
        self.assertEqual(actions[0]['status'], 'rejected_or_failed')
        self.assertFalse(c.objects)
        self.assertEqual(self.backend.execute('SELECT COUNT(*) FROM sales', self.path / 'r')['status'], 'ok')
        self.assertEqual(self.backend.execute('DELETE FROM sales', self.path / 'r')['status'], 'error')

    def test_time_budget_prevents_build(self):
        config = dict(self.config, optimizer_seconds=0)
        c = Controller(self.backend, 'materialization', config)
        fad = receive(prediction(), self.backend.catalog)[0]
        c.observe_fad(1, fad)
        c.observe_fad(2, fad)
        self.assertFalse(c.objects)

    def multiple_directions(self):
        f=prediction()
        other=prediction(groups=False)['candidates'][0]
        other['priority']='low'
        f['candidates'].append(other)
        return receive(f,self.backend.catalog)[0]

    def test_multiple_directions_build_without_waiting_for_next_fad(self):
        c=Controller(self.backend,'materialization',self.config);f=self.multiple_directions()
        c.observe_fad(1,f);actions=c.observe_fad(2,f)
        self.assertEqual([a['status'] for a in actions],['built','built'])
        self.assertEqual(len(c.objects),2)
        self.assertTrue(self.assert_same('SELECT category,SUM(amount) AS s FROM sales GROUP BY category',c))
        self.assertTrue(self.assert_same('SELECT SUM(amount) AS s FROM sales',c))

    def test_multiple_builds_obey_family_budget(self):
        c=Controller(self.backend,'materialization',dict(self.config,max_materialization_objects=1))
        f=self.multiple_directions();c.observe_fad(1,f);actions=c.observe_fad(2,f)
        self.assertEqual(len(c.objects),1)
        self.assertIn('object count budget',actions[1]['reason'])

    def test_time_spent_on_first_build_prevents_second_build(self):
        from unittest.mock import patch
        c=Controller(self.backend,'materialization',dict(self.config,optimizer_seconds=1))
        f=self.multiple_directions();c.observe_fad(1,f)
        clock=[100.];original=c.build
        def build(action,step):
            obj=original(action,step);clock[0]+=1.1;return obj
        with patch('agent_db_tool.optimization.controller.time.perf_counter',side_effect=lambda:clock[0]),patch.object(c,'build',side_effect=build):
            actions=c.observe_fad(2,f)
        self.assertEqual(len(c.objects),1)
        self.assertEqual(actions[1]['reason'],'optimizer time budget reached')
        self.assertGreaterEqual(c.optimizer_seconds,1.1)

    def test_independent_backend_no_materialization_residue(self):
        c = self.build()
        other = TaskBackend(self.path / 'base.sqlite')
        try:
            self.assertEqual(other.execute('SELECT * FROM ' + c.objects[0]['name'], self.path / 'r')['status'], 'error')
        finally:
            other.close()

    def test_result_check_preserves_multiplicity_and_order(self):
        self.assertFalse(compare_results([[1], [1]], [[1], [2]], ['x'], ['x'], False)['equal'])
        self.assertTrue(compare_results([[1], [2]], [[2], [1]], ['x'], ['x'], False)['equal'])
        self.assertFalse(compare_results([[1], [2]], [[2], [1]], ['x'], ['x'], True)['equal'])
        self.assertFalse(compare_results([[40455.]], [[40454.]], ['x'], ['x'], True)['equal'])

    def test_rounding_guard_only_originally_unindexed_tables(self):
        sql = 'SELECT ROUND(SUM(amount),0) AS s FROM sales'
        self.assertIn('NOT INDEXED', preserve_rounding_scan_order(sql, {'sales'})[0])
        self.assertEqual(preserve_rounding_scan_order(sql, set())[0], sql)
        sql = 'SELECT amount FROM sales ORDER BY amount'
        self.assertEqual(preserve_rounding_scan_order(sql, {'sales'})[0], sql)


if __name__ == '__main__':
    unittest.main()
