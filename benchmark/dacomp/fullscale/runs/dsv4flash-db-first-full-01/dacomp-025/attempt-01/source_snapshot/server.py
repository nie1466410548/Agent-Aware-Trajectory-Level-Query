"""Minimal stdio MCP server exposing only logged DAComp data/workspace tools."""
import json, os, select, signal, socket, subprocess, sys, tempfile, time, traceback, uuid
from pathlib import Path
from common import *
from engine import Engine

def schema(props,required=()): return {'type':'object','properties':props,'required':list(required),'additionalProperties':False}
STR={'type':'string'}
TOOLS=[
 {'name':'query_db','description':'Execute SQLite SQL on the supplied read-only database. All statements, bound parameters and full row arrays are archived. Multiple statements and parameter batches are recorded individually. Result preview is limited; complete results are available to Python via db.rows/db.frame.', 'inputSchema':schema({'sql':STR,'parameters':{'anyOf':[{'type':'array','items':{}},{'type':'object'}]},'many':{'type':'array','items':{'anyOf':[{'type':'array','items':{}},{'type':'object'}]}}},['sql'])},
 {'name':'list_db','description':'List database tables and schema via recorded metadata SQL.','inputSchema':schema({})},
 {'name':'python','description':'Run analysis Python for visualization or SQL-unsupported statistics. Explain why outside SQL. Globals: db.query(sql, parameters=[]), db.executemany(sql, parameter_sets), db.executescript(sql), db.rows(result), db.frame(result). Complete archives at /results/<S>.rows.jsonl; save figures in /work using relative paths. Available numpy, pandas, scipy, matplotlib, seaborn. Raw SQLite/network/subprocess access unavailable.','inputSchema':schema({'reason':STR,'code':STR},['reason','code'])},
 {'name':'file','description':'Read or write task workspace files; read result archives in chunks. Workspace paths are relative. Results can be read as results/S1.rows.jsonl.','inputSchema':schema({'path':STR,'content':STR,'offset':{'type':'integer'},'limit':{'type':'integer'}},['path'])},
 {'name':'answer','description':'Submit the final Markdown report. Reference figures by relative workspace paths. Stop after submission.','inputSchema':schema({'markdown':STR},['markdown'])}
]
class Server:
 def __init__(self,run):
    self.run=Path(run); self.meta=json.loads((self.run/'task_meta.json').read_text()); self.work=self.run/'work'; self.work.mkdir(exist_ok=True)
    self.engine=Engine(self.run,Path(self.meta['database_path']),self.meta)
 def python(self,args,call):
    (self.run/'python').mkdir(exist_ok=True)
    pnum=sum(c.get('tool')=='python' for c in records(self.run/'tool_calls.jsonl'))+1; pid=f'P{pnum}'
    (self.run/'python'/f'{pid}.py').write_text(args['code']); dump(self.run/'python'/f'{pid}.json',{'reason':args['reason'],'call_id':call})
    parent,child=socket.socketpair(); stream=parent.makefile('rwb',buffering=0)
    root=tempfile.mkdtemp(prefix='dacomp-sandbox-')
    cmd=['unshare','--user','--map-root-user','--mount','--net','--pid','--fork','--kill-child',str(PYTHON),str(Path(__file__).with_name('sandbox.py')),'launch',root,str(self.work),str(self.run/'results'),str(Path(__file__).with_name('sandbox.py')),str(BENCH/'.venv'),str(child.fileno())]
    with (self.run/'python'/f'{pid}.stdout').open('wb') as out, (self.run/'python'/f'{pid}.stderr').open('wb') as err:
        proc=subprocess.Popen(cmd,pass_fds=[child.fileno()],stdout=out,stderr=err,start_new_session=True,env={'PATH':'/usr/bin:/bin'})
        append(self.run/'child_processes.jsonl',{'pid':proc.pid,'tool_call_id':call,'started_at':time.time()}); child.close()
        stream.write((json.dumps(args)+'\n').encode()); deadline=min(time.time()+self.meta.get('python_timeout_s',180),self.meta.get('deadline',float('inf'))); timed=False
        try:
            while proc.poll() is None:
                if time.time()>deadline: timed=True; break
                if select.select([parent],[],[],0.1)[0]:
                    try: line=stream.readline()
                    except ConnectionResetError: break
                    if not line: break
                    try:
                        req=json.loads(line); response=self.engine.query(req['sql'],req.get('parameters',[]),call,'python',req.get('many'))
                    except Exception as e: response={'error':repr(e)}
                    stream.write((json.dumps(response,default=str)+'\n').encode())
            if timed: os.killpg(proc.pid,signal.SIGKILL)
            proc.wait(timeout=5)
        finally:
            if proc.poll() is None: os.killpg(proc.pid,signal.SIGKILL); proc.wait()
            stream.close(); parent.close()
            try: os.rmdir(root)
            except OSError: pass
    return {'python_id':pid,'returncode':proc.returncode,'timed_out':timed,'stdout':(self.run/'python'/f'{pid}.stdout').read_text(errors='replace')[:18000], 'stderr':(self.run/'python'/f'{pid}.stderr').read_text(errors='replace')[:8000], 'files':sorted(str(p.relative_to(self.work)) for p in self.work.rglob('*') if p.is_file())}
 def call(self,name,args,rpc_id):
    call=uuid.uuid4().hex; e={'call_id':call,'mcp_request_id':rpc_id,'tool':name,'arguments':args,'start_time':time.time()}
    append(self.run/'tool_journal.jsonl',dict(e,record='request'))
    try:
        if time.time()>self.meta.get('deadline',float('inf')): raise TimeoutError('Task deadline')
        if name=='query_db': result=self.engine.query(args['sql'],args.get('parameters',[]),call,many=args.get('many'))
        elif name=='list_db': result=self.engine.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name",[],call,'list_db','metadata')
        elif name=='python': result=self.python(args,call)
        elif name=='answer':
            if not args['markdown'].strip(): raise ValueError('Empty answer')
            (self.run/'answer.md').write_text(args['markdown']); (self.work/'answer.md').write_text(args['markdown']); result={'submitted':True,'file':'work/answer.md'}
        elif name=='file':
            path=Path(args['path']); base=self.run if str(path).startswith('results/') else self.work; path=(base/path).resolve()
            if not path.is_relative_to(base.resolve()): raise ValueError('Path outside allowed workspace')
            if base==self.run and not path.is_relative_to((self.run/'results').resolve()): raise ValueError('Only results allowed')
            if 'content' in args:
                if base==self.run: raise ValueError('Results are read only')
                path.parent.mkdir(parents=True,exist_ok=True); path.write_text(args['content']); result={'written':args['path']}
            else:
                with path.open() as f: f.seek(max(0,args.get('offset',0))); result={'text':f.read(min(args.get('limit',16000),30000)),'next_offset':f.tell(),'bytes':path.stat().st_size}
        else: raise ValueError('Unknown tool')
        e.update(status='success',result=result)
    except Exception as exc: result={'error':repr(exc)}; e.update(status='failed',error=repr(exc))
    e.update(end_time=time.time()); append(self.run/'tool_calls.jsonl',e); append(self.run/'tool_journal.jsonl',dict(e,record='completion'))
    return {'content':[{'type':'text','text':json.dumps({'call_id':call,**result},ensure_ascii=False,default=str)}],'isError':e['status']=='failed'}
 def serve(self):
    for line in sys.stdin:
        try:
            req=json.loads(line); method=req.get('method'); ident=req.get('id')
            if method=='initialize': result={'protocolVersion':'2024-11-05','capabilities':{'tools':{}},'serverInfo':{'name':'dacomp-recorded','version':'1.0.0'}}
            elif method=='tools/list': result={'tools':TOOLS}
            elif method=='tools/call': result=self.call(req['params']['name'],req['params'].get('arguments',{}),ident)
            elif method=='ping': result={}
            else:
                if ident is None: continue
                raise ValueError('Unsupported method '+str(method))
            if ident is not None: print(json.dumps({'jsonrpc':'2.0','id':ident,'result':result},ensure_ascii=False),flush=True)
        except Exception as e:
            print(json.dumps({'jsonrpc':'2.0','id':req.get('id'),'error':{'code':-32603,'message':repr(e)}}),flush=True)
    self.engine.close()
if __name__=='__main__': Server(sys.argv[1]).serve()
