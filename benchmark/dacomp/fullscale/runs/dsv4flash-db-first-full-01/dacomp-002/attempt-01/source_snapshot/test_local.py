"""Semantic acceptance tests, without any model invocation."""
import json, sqlite3, tempfile, time, unittest
from pathlib import Path
from common import *
from engine import Engine
from profile import features
from server import Server
class Tests(unittest.TestCase):
 def setUp(self):
    self.tmp=tempfile.TemporaryDirectory(prefix='dacomp-test-'); self.root=Path(self.tmp.name); self.run=self.root/'run'; self.run.mkdir(); self.db=self.root/'source.sqlite'
    d=sqlite3.connect(self.db); d.executescript('CREATE TABLE t(k TEXT, x REAL, z INT); INSERT INTO t VALUES ("a",2,1),("a",NULL,2),("b",4,1),("b",8,2); CREATE TABLE u(k TEXT, y INT); INSERT INTO u VALUES ("a",5),("b",6)');d.close()
    self.meta={'task_id':'local-test','batch':BATCH,'phase':'local_test','database_path':str(self.db),'deadline':time.time()+60}
    dump(self.run/'task_meta.json',self.meta); self.e=Engine(self.run,self.db,self.meta)
    self.tables=[{'name':'t','columns':['k','x','z']},{'name':'u','columns':['k','y']}]
 def tearDown(self): self.e.close(); self.tmp.cleanup()
 def test_logging(self):
    self.e.query('SELECT ? AS x, ? AS x; SELECT :v',[], 'bad')
    r=self.e.query("SELECT ? AS x, ? AS x",[7,"O'Reilly"],'bound')
    self.e.query('SELECT ?',[], 'batch',many=[[1],[2],[None]])
    self.e.query('select nope from t',[],'failure')
    self.e.execute('SELECT name FROM sqlite_master',[],'list','list_db','metadata')
    es=records(self.run/'sql_events.jsonl'); js=records(self.run/'sql_journal.jsonl')
    self.assertEqual(len(es),9); self.assertEqual(len({e['sql_id'] for e in es}),9)
    self.assertEqual(sum(e['status']=='success' for e in es),6)
    self.assertEqual(sum(j['record']=='request' for j in js),9)
    b=es[3]; self.assertEqual(b['columns'],['x','x']); self.assertEqual(b['parameters'],[7,"O'Reilly"]); self.assertIn("O''Reilly",b['engine_statements'][0])
    self.assertEqual(json.loads((self.run/b['result_file']).read_text()),[7,"O'Reilly"])
    self.assertEqual(self.e.query('ATTACH DATABASE ":memory:" AS bypass',[],'deny')['executions'][0]['status'],'failed')
 def test_structure(self):
    f=features('WITH a AS (SELECT k, SUM(x) AS sx FROM t GROUP BY 1) SELECT a.k, AVG(a.sx) AS avgx FROM a JOIN u ON a.k=u.k GROUP BY a.k',self.tables)
    self.assertTrue(f['parsed'],f); self.assertEqual(set(f['base_tables']),{'t','u'}); self.assertEqual(f['max_join_inputs'],2); self.assertEqual(f['group_dimensions'],[1,1])
    avg=next(a for a in f['aggregate_expressions'] if a['function']=='AVG'); self.assertEqual(avg['metric_columns'],[{'table':'t','column':'x'}])
    f=features('SELECT a.k AS dim, COUNT(*),COUNT(DISTINCT a.x), SUM(CASE WHEN a.z=1 THEN a.x END), SUM(a.x) OVER (PARTITION BY a.k ORDER BY a.z) FROM t a JOIN t b ON a.k=b.k GROUP BY dim',self.tables)
    self.assertEqual(f['table_references'],{'t':2}); self.assertEqual(f['max_join_inputs'],2); self.assertEqual(f['window_count'],1); self.assertEqual(f['aggregate_functions'],{'COUNT':2,'SUM':1})
    self.assertEqual(f['blocks'][0]['group_by'][0]['expression'],'a.k')
    a=next(a for a in f['aggregate_expressions'] if a['function']=='SUM'); self.assertEqual(a['condition_columns'],[{'table':'t','column':'z'}])
    f=features('SELECT (SELECT MAX(x) FROM t), (SELECT MAX(y) FROM u)',self.tables)
    self.assertEqual(f['max_join_inputs'],0); self.assertEqual(set(f['base_tables']),{'t','u'})
    f=features('SELECT * FROM (t a JOIN t b USING(k)) NATURAL JOIN u',self.tables)
    self.assertEqual(set(f['base_tables']),{'t','u'});self.assertEqual(f['max_join_inputs'],3);self.assertEqual(sum(f['join_types'].values()),2)
 def test_null_avg_rewrite(self):
    db=sqlite3.connect(self.db); expected=db.execute('SELECT AVG(x) FROM t').fetchone()
    db.execute('CREATE TEMP TABLE mv AS SELECT k,SUM(x) s,COUNT(x) n,COUNT(*) alln FROM t GROUP BY k')
    self.assertEqual(expected,db.execute('SELECT SUM(s)/SUM(n) FROM mv').fetchone())
    self.assertNotEqual(expected,db.execute('SELECT SUM(s)/SUM(alln) FROM mv').fetchone())
    self.assertNotEqual(db.execute('SELECT k,x FROM t').fetchall(),db.execute('SELECT k,s FROM mv').fetchall()); db.close()
 def test_candidate_replay_and_rejection(self):
    from opportunities import enumerate_candidates,verify
    qs=[]
    for query in ['SELECT k, SUM(x) AS total, AVG(x) AS average FROM t GROUP BY k ORDER BY k','SELECT z, SUM(x) AS total, AVG(x) AS average FROM t GROUP BY z ORDER BY z']:
        self.e.query(query,[],'candidate')
    for q in records(self.run/'sql_events.jsonl'):
        if q['category']=='data': q['profile']=features(q['sql'],self.tables);qs.append(q)
    cs=enumerate_candidates(qs);c=next(c for c in cs if c['type']=='aggregate MV');verify(c,qs,self.run,self.db)
    self.assertEqual(c['status'],'verified',c)
    c['rewrites'][qs[0]['sql_id']]='SELECT __g0 AS k, 0 AS total, 0 AS average FROM temp.reuse_candidate GROUP BY __g0 ORDER BY __g0'
    verify(c,qs,self.run,self.db);self.assertEqual(c['status'],'rejected_result_mismatch')
 def test_relay_latch(self):
    import http.server,threading,urllib.request,urllib.error
    from proxy import Relay
    calls=[]
    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self,*a): pass
        def do_POST(self):
            calls.append(self.path); self.send_response(429); self.end_headers(); self.wfile.write(b'{"error":{"message":"insufficient quota"}}')
    http=http.server.ThreadingHTTPServer(('127.0.0.1',0),H);threading.Thread(target=http.serve_forever,daemon=True).start()
    relay=Relay(self.run,{'options':{'baseURL':f'http://127.0.0.1:{http.server_port}','apiKey':'test-secret'}})
    try:
        for _ in range(2):
            try: urllib.request.urlopen(urllib.request.Request(relay.base_url+'/chat/completions',data=b'{"model":"test"}',headers={'Content-Type':'application/json'}))
            except urllib.error.HTTPError: pass
        self.assertEqual(len(calls),1); self.assertEqual(relay.stopped['kind'],'quota_interrupted')
        self.assertEqual(sum(r.get('status')=='blocked_local_retry' for r in records(self.run/'provider/requests.jsonl')),1)
        self.assertTrue(all('test-secret' not in p.read_text() for p in (self.run/'provider').iterdir()))
    finally: relay.close();http.shutdown();http.server_close()
 def test_python_isolation_and_broker(self):
    s=Server(self.run)
    code=f'''import json, pathlib
r=db.query("SELECT ? AS v",["bound"])
assert db.rows(r)==[["bound"]]
assert len(db.frame(r))==1
try:
 open({str(self.db)!r}).read()
 raise AssertionError("source exposed")
except (FileNotFoundError,PermissionError): pass
import sqlite3
try:
 sqlite3.connect(":memory:")
 raise AssertionError("bypass allowed")
except PermissionError: pass
import matplotlib.pyplot as plt
plt.plot([1,2]); plt.savefig("check.png")
print("sandbox and broker OK")'''
    result=s.call('python',{'reason':'local sandbox test of visualization','code':code},1)
    data=json.loads(result['content'][0]['text']); self.assertEqual(data.get('returncode'),0,data)
    es=records(self.run/'sql_events.jsonl'); self.assertEqual(len(es),2); self.assertEqual(es[1]['source'],'python'); self.assertTrue((self.run/'work/check.png').exists()); s.engine.close()
if __name__=='__main__':
 suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests); result=unittest.TextTestRunner(verbosity=2).run(suite)
 dump(ROOT/'state/local_tests.json',{'run_at':time.time(),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'passed':result.wasSuccessful()})
 raise SystemExit(not result.wasSuccessful())
