"""Offline audit checks; use the benchmark venv (sqlglot), no model calls."""
import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

HAS_SQLGLOT = importlib.util.find_spec('sqlglot') is not None
if HAS_SQLGLOT:
    from agent_db_tool.matching import analyze, decoded_hint, join_matches, key, sql_features


@unittest.skipUnless(HAS_SQLGLOT, 'offline matcher requires sqlglot; use benchmark venv')
class MatchingTests(unittest.TestCase):
    catalog = {'sales': ['date', 'product', 'revenue', 'product_id'], 'products': ['id']}

    def test_time_bucket_joint_dimensions_and_cte_lineage(self):
        f = sql_features("WITH s AS (SELECT date AS d, product AS p, revenue AS r FROM sales) "
                         "SELECT strftime('%Y-%m',d) AS month,p,SUM(r),COUNT(*) "
                         "FROM s GROUP BY month,p", self.catalog)
        self.assertIn(sorted([key(('time_bucket', 'sales.date', 'month')),
                              key(('column', 'sales.product'))]), f['group_sets'])
        self.assertEqual(set(f['aggregations']), {key(('sum', 'sales.revenue')), key(('count', '*'))})

    def test_count_null_distinct_and_computed_aggregate(self):
        f = sql_features('SELECT COUNT(NULL),COUNT(1),COUNT(DISTINCT product),SUM(revenue*2) FROM sales', self.catalog)
        self.assertEqual(set(f['aggregations']), {key(('count', '*')), key(('count_distinct', 'sales.product'))})
        self.assertEqual(len(f['unsupported']), 2)

    def test_filters_are_atoms_and_having_is_excluded(self):
        f = sql_features("SELECT product,SUM(revenue) FROM sales WHERE 0 < revenue AND "
                         "(product IN ('b','a') OR product IS NULL) GROUP BY product HAVING SUM(revenue)>10", self.catalog)
        self.assertEqual(set(f['filters']), {key(('predicate','sales.revenue','gt',0.0)),
            key(('predicate','sales.product','in',['a','b'])), key(('predicate','sales.product','is_null',None))})

    def test_inner_join_swapped_operands(self):
        a = sql_features('SELECT * FROM sales s JOIN products p ON s.product_id=p.id', self.catalog)
        b = sql_features('SELECT * FROM products p JOIN sales s ON p.id=s.product_id', self.catalog)
        self.assertEqual(a['joins'], b['joins'])
        self.assertEqual(len(a['joins']), 1)

    def test_window_count_is_not_plain_group_aggregate(self):
        f = sql_features('SELECT product,COUNT(*) OVER(PARTITION BY product) FROM sales', self.catalog)
        self.assertEqual(f['aggregations'], [])
        self.assertEqual(f['unsupported'][0]['kind'], 'window')

    def test_partial_join_keeps_known_key_when_later_join_adds_year(self):
        predicted=key(('inner',[['a.region','b.region']]))
        actual=key(('inner',[['a.region','b.region'],['a.year','b.year']]))
        self.assertTrue(join_matches(predicted,actual,partial=True))
        self.assertFalse(join_matches(predicted,actual))
        self.assertFalse(join_matches(predicted,key(('left',[['a.region','b.region']])),partial=True))

    def test_offline_decoding_does_not_invent_status_or_mutate_input(self):
        raw = {'candidates':[{'columns':['sales.product']}]}
        decoded, notes = decoded_hint(raw)
        self.assertEqual(raw['candidates'][0]['columns'], ['sales.product'])
        self.assertEqual(decoded['candidates'][0]['columns']['status'], 'unspecified')
        self.assertTrue(notes)

    def test_current_sql_excluded_joint_grouping_and_invalid_hint_clears_coverage(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d); db = p/'test.sqlite'
            conn = sqlite3.connect(db)
            conn.execute('CREATE TABLE sales (product TEXT, date TEXT, revenue REAL, product_id INTEGER)')
            conn.close()
            (p/'task_meta.json').write_text(json.dumps({'task_id':'test', 'database_path':str(db),
                                                       'catalog':{'sales':self.catalog['sales']}}))
            c = {'tables':['sales'], 'columns':{'status':'known','items':['sales.product']},
                 **{f:{'status':'none','items':[]} for f in ('filters','joins','aggregations')},
                 'group_by':{'status':'known','items':[{'type':'column','column':'sales.product'}]},'priority':'high'}
            hint = {'status':'provided','coverage':'partial_plan','candidates':[c]}
            sqls = ['SELECT product FROM sales GROUP BY product',
                    'SELECT product,date FROM sales GROUP BY product,date',
                    'SELECT product FROM sales GROUP BY product']
            es=[]
            for step, sql in enumerate(sqls,1):
                # Q2 rejected input still visible offline; clears delivered state.
                es.append({'record':'request','request_id':str(step),'step_id':step,
                    'arguments':{'sql':sql,'future_access':hint if step<3 else {'status':'no_further_access','candidates':[]}},
                    'hint_errors':[] if step!=2 else [{'message':'test rejection'}]})
                es.append({'record':'completion','request_id':str(step),'response':{'status':'ok'}})
            (p/'events.jsonl').write_text('\n'.join(json.dumps(e) for e in es))
            result=analyze(p)
            detail=json.loads((p/'matching/detail.json').read_text())
            self.assertEqual(detail['rows'][0]['fields']['group_by']['matches'], [3])
            self.assertEqual(detail['rows'][1]['fields']['group_by']['matches'], [3])
            self.assertEqual(result['accepted_matching']['group_by']['candidates_with_items'], 1)
            self.assertEqual(result['coverage']['group_by']['latest_delivered'], 1)
            self.assertEqual(result['coverage']['group_by']['latest_predicted'], 2)


if __name__ == '__main__':
    unittest.main()
