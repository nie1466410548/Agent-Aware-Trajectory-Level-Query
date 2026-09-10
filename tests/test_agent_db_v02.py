import copy
import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator
from agent_db_tool.v02 import build_schema, validate
import test_agent_db_tool as v01_tests

CAT={'sales':['date','province','product','revenue','product_id'], 'products':['id','name']}
def field(state,*items):return {'status':state,'items':list(items)}
def candidate():
    return {'tables':['sales'], 'columns':field('known','sales.date','sales.product','sales.revenue'),
        'filters':field('none'),'joins':field('none'),
        'group_by':field('known',{'type':'time_bucket','column':'sales.date','unit':'month'},{'type':'column','column':'sales.product'}),
        'aggregations':field('known',{'function':'sum','column':'sales.revenue'}),'priority':'high'}
def hint(*cs):return {'status':'provided','coverage':'partial_plan','candidates':list(cs or [candidate()])}
def pred(column='sales.province',op='eq',value=None):
    return {'type':'predicate','column':column,'op':op,'value':value or {'status':'unknown'}}

class ContractTests(unittest.TestCase):
    def good(self,x):
        norm,errors,check=validate(x,CAT)
        self.assertEqual(errors,[])
        self.assertIsNotNone(norm)
        return norm,check
    def bad(self,x):self.assertTrue(validate(x,CAT)[1])
    def test_schema_sync(self):
        Draft202012Validator.check_schema(build_schema())
        self.assertEqual(build_schema(),json.loads(Path('agent_db_tool/schema-v0.2.json').read_text()))
    def test_multiple_likely_patterns(self):
        a=candidate();b=candidate()
        a['group_by']['items']=a['group_by']['items'][:1]
        b['group_by']['items']=b['group_by']['items'][1:]
        a['likelihood']=b['likelihood']='high'
        self.good(hint(a,b))
    def test_partial_filter_keeps_grouping_and_aggregate(self):
        c=candidate();c['columns']['items'].append('sales.province')
        c['filters']=field('partial',pred())
        n,_=self.good(hint(c))
        self.assertEqual(n['candidates'][0]['group_by']['status'],'known')
        c['filters']['status']='known';self.bad(hint(c))
    def test_state_constraints(self):
        for state in ('known','partial'):
            c=candidate();c['group_by']=field(state);self.bad(hint(c))
        for state in ('none','unknown'):
            c=candidate();c['group_by']['status']=state;self.bad(hint(c))
        c=candidate();c['group_by']['status']='partial';self.good(hint(c))
    def test_boolean_tree_and_literal_types(self):
        c=candidate();c['columns']['items'].append('sales.province')
        c['filters']=field('known',{'type':'and','items':[
            pred(op='like',value={'status':'known','literal':'South%'}),
            {'type':'or','items':[pred('sales.revenue','between',{'status':'known','literal':[10,20]}),pred('sales.revenue','is_null',{'status':'known','literal':None})]}]})
        self.good(hint(c))
        c['filters']['items'][0]['items'][1]['items'][0]['value']['literal']=[10]
        self.bad(hint(c))
    def test_missing_columns_are_unioned_without_mutating_raw_input(self):
        c=candidate();c['columns']['items'].remove('sales.product')
        raw=hint(c);before=copy.deepcopy(raw)
        n,check=self.good(raw)
        self.assertEqual(raw,before)
        self.assertIn('sales.product',n['candidates'][0]['columns']['items'])
        self.assertEqual(check['column_unions'][0]['added'],['sales.product'])
        again,audit=self.good(n)
        self.assertEqual(again,n);self.assertEqual(audit['column_unions'],[])
    def test_prose_is_still_rejected(self):
        c=candidate();c['condition']='later';self.bad(hint(c))
        c=candidate();c['description']='compare';self.bad(hint(c))
    def test_unknown_columns_remain_partial_and_none_can_mean_no_extra_columns(self):
        c=candidate();c['columns']=field('unknown')
        n,_=self.good(hint(c))
        self.assertEqual(n['candidates'][0]['columns']['status'],'partial')
        c['columns']=field('none');n,_=self.good(hint(c))
        self.assertEqual(n['candidates'][0]['columns']['status'],'known')
        c['filters']=field('unknown');n,_=self.good(hint(c))
        self.assertEqual(n['candidates'][0]['columns']['status'],'partial')
    def test_union_collects_filter_tree_join_and_quoted_refs(self):
        c=candidate();c['columns']=field('none');c['tables'].append('products')
        c['filters']=field('partial',{'type':'and','items':[pred(),pred('sales.revenue','gt',{'status':'known','literal':0})]})
        c['joins']=field('known',{'type':'inner','conditions':[{'left_column':'sales.`product_id`','op':'eq','right_column':'products.id'}]})
        n,_=self.good(hint(c))
        self.assertEqual(set(n['candidates'][0]['columns']['items']),{'sales.date','sales.product','sales.revenue','sales.province','sales.product_id','products.id'})
        c['joins']['items'][0]['conditions'][0]['right_column']='products.missing'
        self.bad(hint(c))
    def test_name_normalization(self):
        c=candidate();c['columns']['items']=['"sales"."date"','sales.`product`','sales.[revenue]']
        n,check=self.good(hint(c))
        self.assertEqual(n['candidates'][0]['columns']['items'],candidate()['columns']['items'])
        self.assertEqual(len(check['normalizations']),3)
        c['group_by']['items'][0]['column']='sales.missing';self.bad(hint(c))
    def test_count_star_exception(self):
        c=candidate();c['group_by']=field('none');c['columns']=field('none')
        c['aggregations']=field('known',{'function':'count','column':'*'})
        self.good(hint(c))
        c['filters']=field('unknown');self.bad(hint(c))
        c['filters']=field('none');c['aggregations']['items'][0]['function']='sum';self.bad(hint(c))
    def test_equijoin(self):
        c=candidate();c['tables'].append('products');c['columns']['items']+=['sales.product_id','products.id']
        c['joins']=field('known',{'type':'left','conditions':[{'left_column':'sales.product_id','op':'eq','right_column':'products.id'}]})
        self.good(hint(c))
        c['joins']['items'][0]['conditions'][0]['op']='lt';self.bad(hint(c))
    def test_empty_hint_states(self):
        for status in ('unknown','no_further_access'):
            self.good({'status':status,'candidates':[]})
            self.bad({'status':status,'coverage':'partial_plan','candidates':[]})

class V02Integration(unittest.TestCase):
    def test_handler_accepts_and_degrades_without_repeating_sql(self):
        fixture=v01_tests.ToolTests();fixture.setUp()
        try:
            h=fixture.handler;h.version='0.2';h.catalog={'sales':['country','amount']}
            c=candidate();c.update(tables=['sales'],columns=field('known','sales.country','sales.amount'),
                group_by=field('known',{'type':'column','column':'sales.country'}),
                aggregations=field('known',{'function':'sum','column':'sales.amount'}))
            args={'sql':'SELECT SUM(amount) FROM sales','future_access':hint(c)}
            self.assertEqual(h.query(args)['result']['rows'],[[35]])
            c['columns']['items'].remove('sales.country')
            r=h.query({'sql':'SELECT COUNT(*) FROM sales','future_access':hint(c)})
            self.assertEqual(r['result']['rows'],[[3]])
            req=[x for x in fixture.events() if x['record']=='request']
            self.assertEqual(len(req),2)
            self.assertNotIn('sales.country',req[-1]['arguments']['future_access']['candidates'][0]['columns']['items'])
            self.assertIn('sales.country',req[-1]['hint_snapshot']['candidates'][0]['columns']['items'])
            self.assertFalse(req[-1]['hint_errors'])
            self.assertEqual(req[-1]['catalog_check']['column_unions'][0]['added'],['sales.country'])
            c['group_by']['items'][0]['column']='sales.missing'
            self.assertEqual(h.query({'sql':'SELECT COUNT(*) FROM sales','future_access':hint(c)})['result']['rows'],[[3]])
            req=[x for x in fixture.events() if x['record']=='request']
            self.assertEqual(len(req),3);self.assertIsNone(req[-1]['hint_snapshot'])
            self.assertTrue(req[-1]['hint_errors'])
        finally:fixture.tearDown()

if __name__=='__main__':unittest.main()
