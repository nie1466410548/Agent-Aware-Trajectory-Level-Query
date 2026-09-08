import unittest
import sqlglot
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify
from characterize import scoped,literals,valuekey,jac
from overlap_features import SCHEMAS

def scopes(sql):
 return scoped({'sql':sql,'database':'sales_pipeline','dialect':'duckdb'},'crmarenapro')

class CharacterizationTests(unittest.TestCase):
 def test_group_position_and_alias_resolve(self):
  a=scopes('SELECT OwnerId,COUNT(*) FROM Opportunity GROUP BY 1')[0]
  b=scopes('SELECT o.OwnerId AS who,COUNT(*) FROM Opportunity o GROUP BY who')[0]
  self.assertEqual(a['keys'],b['keys']);self.assertEqual(a['input'],b['input'])
 def test_refinement_keys_and_input(self):
  a=scopes('SELECT OwnerId,COUNT(*) FROM Opportunity GROUP BY OwnerId')[0]
  b=scopes('SELECT OwnerId,AccountId,COUNT(*) FROM Opportunity GROUP BY OwnerId,AccountId')[0]
  self.assertLess(set(a['keys']),set(b['keys']));self.assertEqual(a['input'],b['input'])
 def test_predicates_part_of_mv_input(self):
  a=scopes("SELECT OwnerId,COUNT(*) FROM Opportunity WHERE AccountId='a' GROUP BY OwnerId")[0]
  b=scopes("SELECT OwnerId,COUNT(*) FROM Opportunity WHERE AccountId='b' GROUP BY OwnerId")[0]
  self.assertNotEqual(a['input'],b['input'])
 def test_distinct_not_mergeable(self):
  a=scopes('SELECT OwnerId,COUNT(DISTINCT AccountId) FROM Opportunity GROUP BY OwnerId')[0]
  self.assertFalse(a['aggregates']);self.assertTrue(a['unsupported_aggregates'])
 def test_aggregate_filter_preserved(self):
  a=scopes("SELECT OwnerId,COUNT(*) FILTER (WHERE AccountId='a') FROM Opportunity GROUP BY OwnerId")[0]
  self.assertIn('FILTER',a['aggregates'][0])
 def test_dependency_literals_not_arbitrary_constants(self):
  a=literals("SELECT 'irrelevant' FROM t WHERE country='Canada' AND year IN (2020,2021)",'sqlite')
  self.assertEqual({tuple(x['key']) for x in a},{('string','Canada'),('number','2020'),('number','2021')})
  self.assertNotEqual(valuekey(1),valuekey('1'));self.assertIsNone(valuekey(True))
 def test_empty_jaccard_not_perfect_overlap(self):
  self.assertIsNone(jac(set(),set()))
 def test_sqlite_rowid_hidden_from_star(self):
  schema=SCHEMAS['PATENTS','publication_database']
  star=qualify(sqlglot.parse_one('SELECT * FROM publicationinfo',read='sqlite'),schema=schema,dialect='sqlite')
  self.assertNotIn('rowid',{x.name for x in star.find_all(exp.Column)})
  query=qualify(sqlglot.parse_one('SELECT rowid FROM publicationinfo',read='sqlite'),schema=schema,dialect='sqlite')
  self.assertEqual(next(query.find_all(exp.Column)).table,'publicationinfo')

if __name__=='__main__':unittest.main()
