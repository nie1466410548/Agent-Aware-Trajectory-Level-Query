import sys,tempfile,sqlite3,json,threading,http.server,subprocess,pathlib,shutil
sys.path.insert(0,str(pathlib.Path('benchmark/dacomp/fullscale/tools').resolve()))
from common import *
import run
from resume_worker import ResumeRelay
results=[]
with tempfile.TemporaryDirectory() as td:
 temp=Path(td)
 for tid in ['dacomp-087','dacomp-091','dacomp-092','dacomp-093']:
  r=ROOT/'runs'/BATCH/tid/'attempt-01';summary=json.loads((r/'run_summary.json').read_text());session=summary['session_ids'][0]
  captured=[]
  class Handler(http.server.BaseHTTPRequestHandler):
   def log_message(self,*args):pass
   def do_POST(self):
    captured.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
    self.send_response(400);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{"error":{"message":"OFFLINE_VALIDATION_STOP","type":"invalid_request_error"}}')
  server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
  cfg,env=run.environment(r,f'http://127.0.0.1:{server.server_port}/v1');cfg['mcp']={};env['OPENCODE_CONFIG_CONTENT']=json.dumps(cfg)
  for label in ['CONFIG','DATA','CACHE','STATE']:
   dest=temp/tid/label;dest.mkdir(parents=True);env['XDG_'+label+'_HOME']=str(dest)
  dest=Path(env['XDG_DATA_HOME'])/'opencode';dest.mkdir()
  src=sqlite3.connect(f'file:{ROOT}/runtime/{tid}/data/opencode/opencode.db?mode=ro',uri=True);target=sqlite3.connect(dest/'opencode.db');src.backup(target);target.close();src.close()
  p=subprocess.run([run.CLI,'run','--session',session,'--model',MODEL,'--format','json','--pure','--agent','dacomp-db-first','Offline continuity validation.'],cwd=r,env=env,capture_output=True,text=True,timeout=45)
  server.shutdown()
  assert captured,(tid,p.stderr,p.stdout)
  messages=captured[0]['messages'];assert len(messages)>2 and 'ORIGINAL TASK:' in json.dumps(messages)
  events=[json.loads(s) for s in p.stdout.splitlines() if s.startswith('{')];ids={e['sessionID'] for e in events if e.get('sessionID')};assert ids=={session},ids
  results.append({'task_id':tid,'same_session':True,'history_messages':len(messages),'upstream_network_requests':0,'copied_runtime_only':True})
 fake=temp/'relay/attempt-01';(fake/'provider').mkdir(parents=True);(fake/'provider/R23.request.json').write_text('{}')
 relay=ResumeRelay(fake,{'options':{}});assert relay.count==23;relay.close()
 dump(ROOT/'state/resume_tests.json',{'passed':True,'tests':results,'relay_continues_request_ids':True})
 print(json.dumps(results))
