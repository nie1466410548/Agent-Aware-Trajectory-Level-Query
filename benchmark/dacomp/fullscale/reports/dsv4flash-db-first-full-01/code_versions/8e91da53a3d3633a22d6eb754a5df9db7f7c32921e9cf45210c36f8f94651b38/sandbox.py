"""Linux user/mount/network/PID namespace sandbox for analysis Python.
Called under unshare. Only package files, this worker, results and workspace mounted.
The supplied DB, credentials, reports and other attempts are absent.
"""
import ctypes, errno, json, os, socket, sys
from pathlib import Path

def launch():
    root,work,results,worker,venv,fd=sys.argv[2:]
    lib=ctypes.CDLL(None,use_errno=True)
    def mount(src,dst,typ=None,flags=0,data=None):
        args=[x.encode() if isinstance(x,str) else x for x in [src,dst,typ]]
        if lib.mount(*args,ctypes.c_ulong(flags),data)!=0: raise OSError(ctypes.get_errno(),f'mount {src} {dst}')
    mount(None,'/',None,16384|262144) # private recursive mount propagation
    mount('tmpfs',root,'tmpfs',0,b'size=2G')
    def bind(src,dst,write=False):
        target=Path(root+dst)
        if Path(src).is_dir(): target.mkdir(parents=True,exist_ok=True)
        else: target.parent.mkdir(parents=True,exist_ok=True); target.touch()
        mount(src,str(target),None,4096|16384)
        if not write: mount(None,str(target),None,4096|32|1|(os.statvfs(src).f_flag & 14))
    for p in ['/usr','/lib','/lib64','/etc/fonts','/etc/localtime']:
        if Path(p).exists(): bind(p,p)
    bind(venv,venv); bind(worker,'/worker.py'); bind(work,'/work',True); bind(results,'/results')
    for d in ['tmp','dev','proc']: Path(root+'/'+d).mkdir(exist_ok=True)
    for p in ['null','urandom','random']: bind('/dev/'+p,'/dev/'+p,True)
    mount('proc',root+'/proc','proc',0)
    os.chroot(root); os.chdir('/work')
    os.execve(venv+'/bin/python',[venv+'/bin/python','/worker.py','worker',fd],{'PATH':'/usr/bin','MPLBACKEND':'Agg','MPLCONFIGDIR':'/tmp/mpl','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})

def worker():
    fd=int(sys.argv[2]); sock=socket.socket(fileno=fd); stream=sock.makefile('rwb',buffering=0)
    def rpc(payload):
        stream.write((json.dumps(payload)+'\n').encode()); response=json.loads(stream.readline())
        if 'error' in response: raise RuntimeError(response['error'])
        return response
    class Database:
        def query(self,sql,parameters=None): return rpc({'op':'query','sql':sql,'parameters':parameters or []})
        def executemany(self,sql,parameters): return rpc({'op':'query','sql':sql,'many':parameters,'parameters':[]})
        def executescript(self,sql): return self.query(sql)
        def rows(self,result):
            if 'executions' in result: result=result['executions'][-1]
            if not result.get('result_complete'): raise ValueError('Incomplete result')
            return [json.loads(l) for l in open('/'+result['result_file'])]
        def frame(self,result):
            import pandas as pd
            if 'executions' in result: result=result['executions'][-1]
            return pd.DataFrame(self.rows(result),columns=result['columns'])
    # Python audit supplies an additional explicit restriction; namespace mounts
    # enforce non-access to benchmark data even through native libraries.
    def audit(event,args):
        if event in ['sqlite3.connect','subprocess.Popen','os.system','os.exec','os.fork','socket.connect','socket.bind']:
            raise PermissionError('Use db.query for SQL; no subprocess/network: '+event)
    sys.addaudithook(audit)
    payload=json.loads(stream.readline()); code=payload['code']
    exec(compile(code,'<analysis>','exec'),{'__name__':'__main__','db':Database()})
if __name__=='__main__': launch() if sys.argv[1]=='launch' else worker()
