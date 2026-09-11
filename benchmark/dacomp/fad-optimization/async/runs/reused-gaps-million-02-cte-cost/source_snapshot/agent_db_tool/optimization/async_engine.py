"""Isolated online worker. No SQL trajectory, future gaps, or source path input."""
import copy
import multiprocessing as mp
import queue
import resource
import time
import traceback
from .async_backend import AsyncBackend
from .controller import Controller
from .patterns import receive


class AsyncController(Controller):
    def __init__(self,backend,mode,config,emit):
        self.emit=emit
        super().__init__(backend,mode,config)

    def build(self,action,step):
        began=time.monotonic_ns()
        self.emit({'type':'build_started','step':step,'started_ns':began,'action':copy.deepcopy(action)})
        result=super().build(action,step)
        result['build_started_ns']=began
        result['build_ended_ns']=time.monotonic_ns()
        self.emit({'type':'build_finished','step':step,'object':copy.deepcopy(result)})
        return result


def background(database, mode, config, incoming, outgoing, stop):
    start=time.monotonic_ns();cpu=time.process_time();backend=None;controller=None
    emit=lambda value:outgoing.put(dict(value,time_ns=time.monotonic_ns()))
    try:
        backend=AsyncBackend(database,config['query_seconds'],stop)
        controller=AsyncController(backend,mode,config,emit)
        emit({'type':'worker_ready','started_ns':start,'ended_ns':time.monotonic_ns(),'init_seconds':(time.monotonic_ns()-start)/1e9})
        while not stop.is_set():
            try:message=incoming.get(timeout=.1)
            except queue.Empty:continue
            if message is None or stop.is_set():break
            step,raw,delivered_ns=message
            began=time.monotonic_ns()
            fad,audit=receive(raw,backend.catalog)
            validated=time.monotonic_ns()
            emit({'type':'fad_validated','step':step,'delivered_ns':delivered_ns,
                  'started_ns':began,'ended_ns':validated,'fad':fad,'audit':audit})
            before=len(controller.objects)
            observed=time.monotonic_ns()
            decisions=controller.observe_fad(step,fad)
            finished=time.monotonic_ns()
            # The trusted connection translated TEMP to committed task tables.
            for obj in controller.objects[before:]:
                commit=backend.db.commits.get(obj['ddl'],{})
                obj.update(commit)
                obj['ddl']=commit.get('actual_ddl',obj['ddl'])
                obj['ready_ns']=finished
                emit({'type':'object_ready','step':step,'object':copy.deepcopy(obj)})
            emit({'type':'decision','step':step,'delivered_ns':delivered_ns,
                  'started_ns':observed,'ended_ns':finished,'actions':decisions,
                  'extra_allocated_bytes':backend.space()})
        cleanup_start=time.monotonic_ns()
        if controller:controller.cleanup()
        if backend:backend.close();backend=None
        emit({'type':'worker_closed','cleanup_started_ns':cleanup_start,
              'cleanup_ended_ns':time.monotonic_ns(),'cpu_seconds':time.process_time(),'worker_body_cpu_seconds':time.process_time()-cpu,
              'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    except BaseException:
        emit({'type':'worker_error','traceback':traceback.format_exc()})
        if backend:
            try:backend.close()
            except Exception:pass
        raise


class AsyncEngine:
    def __init__(self,database,mode,config):
        context=mp.get_context('spawn')
        self.incoming=context.Queue();self.outgoing=context.Queue();self.stop=context.Event()
        self.process=context.Process(target=background,args=(str(database),mode,config,self.incoming,self.outgoing,self.stop))
        self.ready={};self.events=[];self.process.start()

    def submit(self,step,raw):
        delivered=time.monotonic_ns()
        self.incoming.put((step,raw,delivered))
        return delivered

    def poll(self):
        new=[]
        while True:
            try:e=self.outgoing.get_nowait()
            except queue.Empty:break
            self.events.append(e);new.append(e)
            if e['type']=='object_ready':self.ready[e['object']['name']]=e['object']
        return new

    def available(self,before_ns):
        self.poll()
        return [copy.deepcopy(o) for o in self.ready.values() if o['ready_ns']<=before_ns]

    def close(self):
        self.stop.set();self.incoming.put(None)
        deadline=time.monotonic()+30
        while self.process.is_alive() and time.monotonic()<deadline:
            self.poll();self.process.join(.05)
        forced=self.process.is_alive()
        if forced:self.process.terminate();self.process.join(5)
        self.poll()
        result={'exit_code':self.process.exitcode,'forced_termination':forced,
                'closed_event':any(e['type']=='worker_closed' for e in self.events),
                'errors':[e for e in self.events if e['type']=='worker_error']}
        self.incoming.close();self.outgoing.close()
        return result
