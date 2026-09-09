"""No model calls: cross-task quota latch and duplicate-safe scheduler smoke test."""
import http.server,json,tempfile,threading,urllib.request,urllib.error,unittest,subprocess,sys,os
from pathlib import Path
from unittest.mock import patch
from parallel_worker import BatchRelay
import parallel_run as scheduler

class ParallelTests(unittest.TestCase):
 def test_cross_task_stop(self):
  calls=[]
  class Handler(http.server.BaseHTTPRequestHandler):
   def log_message(self,*args):pass
   def do_POST(self):
    calls.append(1);self.send_response(402);self.end_headers();self.wfile.write(b'{"error":"insufficient quota"}')
  upstream=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=upstream.serve_forever,daemon=True).start()
  with tempfile.TemporaryDirectory() as td:
   root=Path(td)
   with patch.object(BatchRelay,'stop_path',root/'stop.json'):
    relays=[]
    try:
     for tid in ['a','b']:
      run=root/tid/'attempt-01';run.mkdir(parents=True)
      relays.append(BatchRelay(run,{'options':{'baseURL':f'http://127.0.0.1:{upstream.server_port}','apiKey':'FAKE_LOCAL_TEST_ONLY'}}))
     for relay in relays:
      try:urllib.request.urlopen(urllib.request.Request(relay.base_url+'/chat/completions',data=b'{}',method='POST'),timeout=5)
      except urllib.error.HTTPError as error:self.assertEqual(error.code,400)
     self.assertEqual(len(calls),1)
     self.assertEqual(relays[1].stopped['kind'],'quota_interrupted')
     self.assertTrue(relays[1].stopped['propagated'])
     self.assertNotIn('FAKE_LOCAL_TEST_ONLY',''.join(p.read_text() for p in root.rglob('*') if p.is_file()))
    finally:
     for relay in relays:relay.close()
  upstream.shutdown();upstream.server_close()
 def test_scheduler_once(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);(root/'state').mkdir();(root/'tools').mkdir()
   tids=['dacomp-001','dacomp-002','dacomp-003','dacomp-004','dacomp-005']
   (root/'state/queue.json').write_text(json.dumps({'tasks':{t:{'status':'submitted' if i==0 else 'pending'} for i,t in enumerate(tids)},'order':tids}))
   for name in ['acceptance','local_tests']:(root/f'state/{name}.json').write_text('{"passed":true}')
   (root/'tools/report.py').write_text('')
   (root/'tools/parallel_worker.py').write_text('''import sys,time,json,os
from pathlib import Path
root=Path(__file__).resolve().parents[1];tid=sys.argv[1]
r=root/'runs'/'dsv4flash-db-first-full-01'/tid/'attempt-01';r.mkdir(parents=True,exist_ok=False)
(r/'begin').write_text(str(time.time()));time.sleep(.5)
(r/'run_summary.json').write_text(json.dumps({'status':'submitted'}));(r/'end').write_text(str(time.time()))
''')
   with patch.object(scheduler,'ROOT',root),patch.object(scheduler,'PYTHON',Path(sys.executable)),patch.object(sys,'argv',['parallel_run.py','--concurrency','3']):scheduler.main()
   q=json.loads((root/'state/queue.json').read_text());self.assertEqual(sum(v['status']=='submitted' for v in q['tasks'].values()),5)
   runs=list((root/'runs').glob('*/*/attempt-01'));self.assertEqual(len(runs),4)
   self.assertFalse((root/'runs'/'dsv4flash-db-first-full-01'/tids[0]).exists())
   starts=sorted(float((r/'begin').read_text()) for r in runs);ends=sorted(float((r/'end').read_text()) for r in runs)
   self.assertLess(starts[2],ends[0],'Three attempts should overlap')
if __name__=='__main__':unittest.main()
