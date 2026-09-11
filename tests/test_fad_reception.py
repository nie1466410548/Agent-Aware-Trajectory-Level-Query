import copy
import unittest
from agent_db_tool.optimization.patterns import receive
from test_fad_optimization import prediction


class ReceptionTest(unittest.TestCase):
    catalog={'sales':['category','amount']}

    def test_explicit_operations_fill_empty_known_columns_without_mutation(self):
        raw=prediction();raw['candidates'][0]['columns']['items']=[];before=copy.deepcopy(raw)
        fad,audit=receive(raw,self.catalog)
        self.assertIsNotNone(fad);self.assertEqual(raw,before)
        self.assertEqual(set(fad['candidates'][0]['columns']['items']),{'sales.category','sales.amount'})
        self.assertTrue(audit['normalizations'])

    def test_singleton_logic_and_unknown_value_remain_uncertain(self):
        raw=prediction();c=raw['candidates'][0]
        c['filters']={'status':'known','items':[{'type':'and','items':[{
            'type':'predicate','column':'sales.category','op':'eq','value':{'status':'unknown','literal':'a'}}]}]}
        fad,audit=receive(raw,self.catalog);self.assertIsNotNone(fad)
        f=fad['candidates'][0]['filters']
        self.assertEqual(f['status'],'partial');self.assertEqual(f['items'][0]['type'],'predicate')
        self.assertEqual(f['items'][0]['value'],{'status':'unknown'})

    def test_bad_candidate_does_not_discard_good_candidate_or_weaken_and(self):
        raw=prediction();raw['coverage']='remaining_task';bad=copy.deepcopy(raw['candidates'][0])
        good={'type':'predicate','column':'sales.category','op':'eq','value':{'status':'known','literal':'a'}}
        invalid=copy.deepcopy(good);invalid['column']='sales.nonexistent'
        bad['filters']={'status':'known','items':[{'type':'and','items':[good,invalid]}]}
        raw['candidates'].insert(0,bad)
        fad,audit=receive(raw,self.catalog)
        self.assertEqual(len(fad['candidates']),1);self.assertEqual(audit['accepted_candidate_indices'],[2])
        self.assertEqual(audit['rejected_candidates'][0]['candidate'],1)
        self.assertEqual(fad['coverage'],'partial_plan')
        self.assertEqual(fad['candidates'][0]['filters']['status'],'none')

    def test_invalid_envelope_and_size_still_rejected(self):
        raw=prediction();raw['candidates']*=9
        self.assertIsNone(receive(raw,self.catalog)[0])
        raw=prediction();raw['extra']='x'
        self.assertIsNone(receive(raw,self.catalog)[0])
        raw=prediction();raw['candidates'][0]['columns']['items']=['x'*17000]
        self.assertIsNone(receive(raw,self.catalog)[0])

    def test_empty_columns_without_explicit_references_not_invented(self):
        raw=prediction(groups=False,functions=('count',));c=raw['candidates'][0]
        c['columns']['items']=[];c['aggregations']['items'][0]['column']='*'
        self.assertIsNone(receive(raw,self.catalog)[0])

if __name__=='__main__':unittest.main()
