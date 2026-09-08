"""Semantic-boundary checks for static candidates; not performance tests."""
import unittest
from discover import extract
from tool import execute_mongo
from analyze import mongo_features

def q(sql):return {'sql':sql,'database':'sales_pipeline','dialect':'duckdb'}

def states(sql):return {(x['relation'],x['object']) for x in extract(q(sql),'crmarenapro') if x['kind']=='aggregate_state'}

class AnalysisTests(unittest.TestCase):
 def test_count_on_different_tables_not_shared_state(self):
  self.assertFalse(states('SELECT COUNT(*) FROM Opportunity') & states('SELECT COUNT(*) FROM Contract'))
 def test_different_group_not_shared_state(self):
  self.assertFalse(states('SELECT OwnerId,COUNT(*) FROM Opportunity GROUP BY OwnerId') & states('SELECT AccountId,COUNT(*) FROM Opportunity GROUP BY AccountId'))
 def test_different_filter_not_shared_state(self):
  self.assertFalse(states("SELECT COUNT(*) FROM Opportunity WHERE OwnerId='A'") & states("SELECT COUNT(*) FROM Opportunity WHERE OwnerId='B'"))
 def test_aliases_same_input_same_state(self):
  self.assertEqual(states('SELECT o.OwnerId,COUNT(*) FROM Opportunity o GROUP BY o.OwnerId'),states('SELECT a.OwnerId,COUNT(*) FROM Opportunity a GROUP BY a.OwnerId'))
 def test_aggregate_filter_is_part_of_state(self):
  a=states("SELECT COUNT(*) FILTER (WHERE OwnerId='A') FROM Opportunity")
  b=states("SELECT COUNT(*) FILTER (WHERE OwnerId='B') FROM Opportunity")
  self.assertTrue(a)
  self.assertFalse(a & b)
  self.assertFalse(a & states('SELECT COUNT(*) FROM Opportunity'))
  self.assertEqual(a,states("SELECT COUNT(*) FILTER (WHERE o.OwnerId='A') FROM Opportunity o"))
  self.assertFalse(states('SELECT COUNT(*) FILTER (WHERE random() > 0.5) FROM Opportunity'))
 def test_left_join_not_inner_join_candidate(self):
  items=extract(q('SELECT o.Id,c.Id FROM Opportunity o LEFT JOIN Contract c ON c.Id=o.ContractID__c'),'crmarenapro')
  self.assertFalse(any(x['kind']=='join' for x in items))
 def test_volatile_aggregate_not_shared_state(self):
  self.assertFalse(states('SELECT SUM(random()) FROM Opportunity'))
  self.assertFalse(states('SELECT COUNT(*) FROM Opportunity WHERE CAST(CreatedDate AS DATE) < CURRENT_DATE'))
 def test_rejected_mongo_attempt_remains_recorded(self):
  row=mongo_features({'call_id':'rejected','tool':'query-db','dialect':'mongo','success':False,'sql':None})
  self.assertFalse(row['success'])
  self.assertEqual(row['mongo_request']['operation'],'unknown')
  self.assertEqual(row['tables'],[])
 def test_mongo_nested_write_rejected_before_connection(self):
  with self.assertRaises(ValueError):execute_mongo({}, {'operation':'aggregate','pipeline':[{'$lookup':{'from':'x','pipeline':[{'$merge':'y'}]}}]})
if __name__=='__main__':unittest.main()
