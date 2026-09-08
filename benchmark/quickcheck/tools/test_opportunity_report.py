"""Counting/provenance safeguards; these do not validate optimization equivalence."""
import copy
import json
import unittest
from opportunity_report import ROOT, validate_candidate, stats
from opportunity_catalog import CANDIDATES

class OpportunityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runs={}
        for path in (ROOT/'runs').glob('*/*/*/quick-01/analysis.json'):
            r=json.loads(path.read_text());r['directory']=path.parent
            cls.runs[r['summary']['group'],r['summary']['task_id']]=r

    def test_different_database_not_accepted(self):
        c=copy.deepcopy(CANDIDATES[0]);c['database']='review_database'
        with self.assertRaises(AssertionError):validate_candidate(c,self.runs)

    def test_unrelated_input_not_accepted(self):
        c=copy.deepcopy(CANDIDATES[0]);c['tables']=['review']
        with self.assertRaises(AssertionError):validate_candidate(c,self.runs)

    def test_same_call_not_multiple_consumers(self):
        c=copy.deepcopy(CANDIDATES[0]);c['members']=[4,4]
        with self.assertRaises(AssertionError):validate_candidate(c,self.runs)

    def test_overlapping_families_do_not_double_count_coverage(self):
        c=validate_candidate(CANDIDATES[0],self.runs)
        one=stats([c],self.runs,'natural','A')
        two=stats([c,dict(c,id='extra')],self.runs,'natural','A')
        self.assertEqual(one['covered_calls'],two['covered_calls'])
        self.assertEqual(one['later_calls'],two['later_calls'])
        self.assertEqual(two['families'],2)

if __name__=='__main__':unittest.main()
