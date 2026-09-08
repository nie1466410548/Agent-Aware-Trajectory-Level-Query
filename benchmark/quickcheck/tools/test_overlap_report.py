import json
from pathlib import Path
import tempfile
import unittest
from overlap_report import enrich

class BindingTests(unittest.TestCase):
    def feature(self, sql, dataset='crmarenapro', database='sales_pipeline', dialect='duckdb'):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'results').mkdir();(root/'results/test.json').write_text('[]')
            return enrich({'sql':sql,'database':database,'dialect':dialect,'call_id':'test'},dataset,root)

    def test_same_named_columns_retain_table(self):
        q=self.feature('SELECT o.Id, c.Id FROM Opportunity o JOIN Contract c ON o.ContractID__c=c.Id')
        self.assertIn(('opportunity','id'),q['bound_columns'])
        self.assertIn(('contract','id'),q['bound_columns'])

    def test_star_expands_but_count_star_does_not(self):
        self.assertIn(('contract','companysigneddate'),self.feature('SELECT * FROM Contract')['bound_columns'])
        self.assertEqual([],self.feature('SELECT COUNT(*) FROM Contract')['bound_columns'])

    def test_multistatement_and_quoted_case(self):
        q=self.feature('SELECT "CreatedDate" FROM "Opportunity"; SELECT "CompanySignedDate" FROM "Contract"')
        self.assertEqual(2,q['statement_count'])
        self.assertEqual([('contract','companysigneddate'),('opportunity','createddate')],q['bound_columns'])

    def test_alias_normalization_preserves_literals(self):
        a=self.feature("SELECT o.Id FROM Opportunity o WHERE o.Id='ABC'")
        b=self.feature("SELECT x.Id FROM Opportunity x WHERE x.Id='ABC'")
        c=self.feature("SELECT x.Id FROM Opportunity x WHERE x.Id='abc'")
        self.assertEqual(a['bound_filters'],b['bound_filters'])
        self.assertNotEqual(a['bound_filters'],c['bound_filters'])

if __name__=='__main__':unittest.main()
