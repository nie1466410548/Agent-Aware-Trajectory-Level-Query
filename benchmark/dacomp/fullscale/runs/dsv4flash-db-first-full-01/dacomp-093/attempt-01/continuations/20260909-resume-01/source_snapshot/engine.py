"""Single statement journal + SQLite trace; authoritative trajectory accounting."""
import base64, hashlib, json, sqlite3, time, uuid
from pathlib import Path
from common import append, dump, records

def encode(x):
    if isinstance(x,bytes): return {'$blob_base64':base64.b64encode(x).decode()}
    raise TypeError(type(x).__name__)

def split_sql(script):
    start=0
    for i,c in enumerate(script):
        if c==';' and sqlite3.complete_statement(script[start:i+1]):
            s=script[start:i+1]; start=i+1
            if s.strip(): yield s
    if script[start:].strip(): yield script[start:]

def category(sql):
    s=sql.lstrip().lower()
    if s.startswith('pragma'): return 'metadata'
    if s.startswith(('begin','commit','rollback','savepoint','release')): return 'connection_setup'
    if s.startswith(('vacuum','analyze','reindex')): return 'maintenance'
    if 'sqlite_master' in s or 'sqlite_schema' in s or 'pragma_' in s: return 'metadata'
    if s.startswith(('select','with','explain','values')): return 'data'
    return 'unknown'

class Engine:
    def __init__(self,run,dbpath,meta):
        self.run=Path(run); self.meta=meta; self.dbpath=Path(dbpath); self.db=None; self.current=None
        self.seq=max([r.get('sequence',0) for r in records(self.run/'sql_journal.jsonl')]+[0])
        self.nquery=sum(r.get('record')=='request' and r.get('source') not in ['connection','list_db'] for r in records(self.run/'sql_journal.jsonl'))
        self.connection=uuid.uuid4().hex
        for name in ['sql','results']: (self.run/name).mkdir(exist_ok=True)
    def trace(self,sql):
        event={'record':'engine_trace','sql_id':self.current['sql_id'] if self.current else None,'engine_sql':sql,'time':time.time(),'connection_id':self.connection}
        append(self.run/'sql_journal.jsonl',event)
        if self.current is not None: self.current['engine_statements'].append(sql)
    def connect(self,call):
        if self.db is not None: return
        self.db=sqlite3.connect(self.dbpath.resolve().as_uri()+'?mode=ro',uri=True,isolation_level=None)
        self.db.set_trace_callback(self.trace)
        self.execute('PRAGMA query_only=ON',[],call,'connection','connection_setup')
        def auth(action,a,b,*rest):
            if action in {sqlite3.SQLITE_ATTACH,sqlite3.SQLITE_DETACH}: return sqlite3.SQLITE_DENY
            if action==sqlite3.SQLITE_FUNCTION and (b or '').lower() in ['load_extension','readfile','writefile']: return sqlite3.SQLITE_DENY
            if action==sqlite3.SQLITE_PRAGMA and (a or '').lower()=='query_only' and b is not None: return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK
        self.db.set_authorizer(auth)
    def execute(self,sql,parameters,call,source='query_db',kind=None,parent=None):
        if self.db is None: self.connect(call)
        if source not in ['connection','list_db']:
            if self.nquery>=self.meta.get('query_attempt_limit',120):
                rejection={'call_id':call,'sql':sql,'parameters':parameters,'status':'rejected_limit','time':time.time(),'source':source}
                append(self.run/'sql_rejections.jsonl',rejection); return rejection
            self.nquery+=1
        self.seq+=1; sid=f'S{self.seq}'
        e={'batch':self.meta.get('batch'),'task_id':self.meta['task_id'],'attempt':'attempt-01','phase':self.meta.get('phase','agent_trajectory'),
           'call_id':call,'parent_call_id':parent,'sql_id':sid,'sequence':self.seq,'execution_id':uuid.uuid4().hex,'connection_id':self.connection,
           'start_time':time.time(),'source':source,'sql':sql,'parameters':parameters,'database':self.meta['task_id'],'dialect':'sqlite',
           'category':kind or category(sql),'status':'attempted','engine_statements':[],'result_complete':False,'coverage':'wrapper_and_engine_trace'}
        (self.run/'sql'/f'{sid}.sql').write_text(sql)
        dump(self.run/'sql'/f'{sid}.parameters.json',parameters)
        append(self.run/'sql_journal.jsonl',dict(e,record='request')); self.current=e
        start=time.perf_counter(); deadline=min(time.time()+self.meta.get('sql_timeout_s',300),self.meta.get('deadline',float('inf')))
        self.db.set_progress_handler(lambda:int(time.time()>deadline),10000)
        rowsfile=self.run/'results'/f'{sid}.rows.jsonl'; h=hashlib.sha256(); preview=[]; num=0; size=0; encode_ms=0; fetch_ms=0
        try:
            cur=self.db.execute(sql,parameters)
            e['execute_return_ms']=(time.perf_counter()-start)*1000
            e['columns']=[d[0] for d in cur.description] if cur.description else []
            e['declared_result_types']=None; types=[set() for _ in e['columns']]
            with rowsfile.open('wb') as f:
                while True:
                    a=time.perf_counter(); chunk=cur.fetchmany(512); fetch_ms+=(time.perf_counter()-a)*1000
                    if not chunk: break
                    for row in chunk:
                        if time.time()>deadline: raise TimeoutError('SQL deadline during result consumption')
                        a=time.perf_counter(); raw=(json.dumps(row,ensure_ascii=False,default=encode)+'\n').encode()
                        if size+len(raw)>self.meta.get('result_limit_bytes',256*1024*1024): raise OverflowError('result archive limit; incomplete')
                        f.write(raw); h.update(raw); size+=len(raw); num+=1
                        for i,v in enumerate(row): types[i].add(type(v).__name__)
                        if len(preview)<12: preview.append(row)
                        encode_ms+=(time.perf_counter()-a)*1000
                f.flush()
            e.update(status='success',result_complete=True,observed_types=[sorted(t) for t in types])
        except Exception as exc:
            e.update(status='cancelled' if isinstance(exc,TimeoutError) or 'interrupted' in str(exc) else 'limited' if isinstance(exc,OverflowError) else 'failed',error=repr(exc))
        finally:
            e.update(end_time=time.time(),row_count=num if e['result_complete'] else None,archived_rows=num,result_bytes=size,
                     result_file=f'results/{sid}.rows.jsonl' if rowsfile.exists() else None,result_sha256=h.hexdigest() if rowsfile.exists() else None,
                     fetch_ms=fetch_ms,execute_fetch_ms=e.get('execute_return_ms',0)+fetch_ms,encode_write_ms=encode_ms,wall_ms=(time.perf_counter()-start)*1000)
            self.current=None; append(self.run/'sql_journal.jsonl',dict(e,record='completion')); append(self.run/'sql_events.jsonl',e)
        return {k:e.get(k) for k in ['sql_id','status','columns','row_count','archived_rows','result_file','result_complete','error']}|{'preview':preview}
    def query(self,sql,parameters,call,source='query_db',many=None):
        statements=list(split_sql(sql)); answers=[]
        for params in many if many is not None else [parameters]:
            for statement in statements: answers.append(self.execute(statement,params,call,source,parent=call if source=='python' else None))
        return {'executions':answers}
    def close(self):
        if self.db: self.db.close()
