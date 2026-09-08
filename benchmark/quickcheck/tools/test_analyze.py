import unittest
from analyze import features, sql_pairs

def q(sql,call):
    return features({'call_id':str(call),'tool':'query-db','database':'db','sql':sql,'success':True,
        'start_time':call,'duration_ms':1,'dialect':'sqlite','row_count':1})

class CharacterizationTests(unittest.TestCase):
    def test_literals_not_case_folded(self):
        p=sql_pairs([q("SELECT id FROM t WHERE state='CA'",1),q("SELECT id FROM t WHERE state='ca'",2)])
        self.assertNotIn('same_canonical_query',p[0]['reuse_witnesses'])
    def test_sample_not_full_materialization(self):
        p=sql_pairs([q('SELECT id FROM t LIMIT 5',1),q('SELECT id FROM t',2)])
        self.assertEqual(p[0]['reuse_witnesses'],[])
    def test_projection_requirements(self):
        p=sql_pairs([q('SELECT id FROM t',1),q('SELECT id FROM t WHERE score>10',2)])
        self.assertEqual(p[0]['reuse_witnesses'],[])
        p=sql_pairs([q('SELECT id,score FROM t',1),q('SELECT id FROM t WHERE score>10',2)])
        self.assertIn('earlier_full_base_rows_cover_later_single_table_query',p[0]['reuse_witnesses'])
    def test_disjoint_ranges(self):
        p=sql_pairs([q('SELECT id FROM t WHERE year>=2020',1),q('SELECT id FROM t WHERE year<2020',2)])
        self.assertEqual(p[0]['range_comparisons'][0]['relation'],'disjoint')

if __name__=='__main__':unittest.main()
