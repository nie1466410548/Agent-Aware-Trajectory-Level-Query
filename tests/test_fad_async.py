"""Meaningful async boundaries: unfinished builds cannot stall/read partial results."""
import importlib.util
import json
import multiprocessing as mp
import sqlite3
import tempfile
import time
import unittest
import copy
from pathlib import Path

HAS=importlib.util.find_spec('sqlglot') is not None and importlib.util.find_spec('jsonschema') is not None
if HAS:
    from agent_db_tool.optimization.async_backend import AsyncBackend
    from agent_db_tool.optimization.async_engine import AsyncEngine,AsyncController
    from agent_db_tool.optimization.replay import DEFAULT_CONFIG,sha
    from agent_db_tool.optimization.rewrite import rewrite
    from agent_db_tool.optimization.async_replay import worker


def prediction():
    f=lambda s,x:{'status':s,'items':x}
    return {'status':'provided','coverage':'partial_plan','candidates':[{
        'tables':['sales'],'priority':'high','columns':f('known',['sales.amount','sales.kind']),
        'filters':f('none',[]),'joins':f('none',[]),
        'group_by':f('known',[{'type':'column','column':'sales.kind'}]),
        'aggregations':f('known',[{'function':'sum','column':'sales.amount'}])}]}


def held_writer(path,started,release):
    db=sqlite3.connect(path,isolation_level=None)
    db.execute('BEGIN IMMEDIATE')
    db.execute('CREATE TABLE pending AS SELECT kind,SUM(amount) AS total FROM sales GROUP BY kind')
    started.set();release.wait(10);db.execute('COMMIT');db.close()


def two_predictions():
    f=prediction();other=copy.deepcopy(f['candidates'][0])
    other['group_by']={'status':'none','items':[]};other['priority']='low'
    f['candidates'].append(other);return f


def held_second_build(path,started,release,events,stop):
    backend=AsyncBackend(path,stop=stop);count=0
    def emit(e):
        nonlocal count
        events.put(e)
        if e['type']=='build_started':
            count+=1
            if count==2:
                started.set()
                if not release.wait(10):raise TimeoutError('test release missing')
    controller=AsyncController(backend,'materialization',DEFAULT_CONFIG,emit,stop)
    try:
        controller.observe_fad(1,two_predictions());controller.observe_fad(2,two_predictions())
    finally:controller.cleanup();backend.close()


@unittest.skipUnless(HAS,'requires optimization dependencies')
class AsyncTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.path=self.root/'task.sqlite'
        db=sqlite3.connect(self.path);db.execute('CREATE TABLE sales(kind TEXT,amount REAL)')
        db.executemany('INSERT INTO sales VALUES (?,?)',[('a',1.),('b',2.)]*5000);db.commit();db.close()
        self.db=AsyncBackend(self.path)

    def tearDown(self):
        self.db.close();self.tmp.cleanup()

    def test_query_continues_while_write_uncommitted(self):
        ctx=mp.get_context('spawn');started=ctx.Event();release=ctx.Event()
        proc=ctx.Process(target=held_writer,args=(str(self.path),started,release));proc.start()
        try:
            self.assertTrue(started.wait(5))
            self.db.begin_snapshot();r=self.db.execute('SELECT COUNT(*) AS n FROM sales',self.root/'r.jsonl')
            self.assertEqual(r['status'],'ok');self.assertTrue(proc.is_alive())
            self.assertEqual(self.db.execute('SELECT * FROM pending',self.root/'p.jsonl')['status'],'error')
            self.db.end_snapshot();release.set();proc.join(5);self.assertEqual(proc.exitcode,0)
            self.assertEqual(self.db.execute('SELECT * FROM pending',self.root/'p.jsonl')['status'],'ok')
        finally:
            release.set();proc.join(5)
            if proc.is_alive():proc.terminate();proc.join()

    def test_committed_materialization_visible_across_connections(self):
        engine=AsyncEngine(self.path,'materialization',DEFAULT_CONFIG)
        try:
            before=time.monotonic_ns();engine.submit(1,prediction());engine.submit(2,prediction())
            self.assertEqual(engine.available(before),[])
            deadline=time.monotonic()+10
            while not engine.available(time.monotonic_ns()) and time.monotonic()<deadline:time.sleep(.02)
            objects=engine.available(time.monotonic_ns());self.assertEqual(len(objects),1)
            self.assertTrue(objects[0]['ddl'].startswith('CREATE TABLE '))
            self.assertGreaterEqual(objects[0]['ready_ns'],objects[0]['commit_return_ns'])
            sql='SELECT kind,SUM(amount) AS total FROM sales GROUP BY kind'
            changed,used,_=rewrite(sql,objects,self.db.catalog);self.assertTrue(used)
            self.assertEqual(self.db.db.execute(sql).fetchall(),self.db.db.execute(changed).fetchall())
        finally:
            result=engine.close();self.assertTrue(result['closed_event'])
        self.assertEqual(self.db.execute('DELETE FROM sales',self.root/'x')['status'],'error')
        self.assertEqual(self.db.db.execute("SELECT name FROM sqlite_master WHERE name LIKE 'fad_%'").fetchall(),[])

    def test_baseline_uses_real_relative_gaps_without_fad(self):
        self.db.close()
        timing={'source_database_sha256':sha(self.path),'source_wait_seconds':.06,'total_wait_seconds':.06,
                'final_gap_seconds':.02,'calls':[
                    {'step':1,'gap_before_seconds':.02,'arguments':{'sql':'SELECT COUNT(*) AS n FROM sales','future_access':prediction()}},
                    {'step':2,'gap_before_seconds':.02,'arguments':{'sql':'SELECT COUNT(*) AS n FROM sales','future_access':prediction()}}]}
        file=self.root/'timing.json';file.write_text(json.dumps(timing))
        result=worker(self.path,file,self.root/'run','baseline')
        self.assertGreaterEqual(result['task_wall_seconds'],.06)
        timeline=json.loads((self.root/'run/timeline.json').read_text())
        self.assertFalse(timeline['background'])
        self.assertTrue(all(r['raw_fad'] is None for r in timeline['queries']))
        q1,q2=timeline['queries'];self.assertGreaterEqual(q2['arrival_ns']-q1['response_return_ns'],19_900_000)

    def test_idle_gaps_reused_after_real_background_completion(self):
        self.db.close()
        timing={'source_database_sha256':sha(self.path),'total_wait_seconds':240,
                'final_gap_seconds':60,'calls':[
                    {'step':i,'gap_before_seconds':60,'arguments':{
                        'sql':'SELECT kind,SUM(amount) AS total FROM sales GROUP BY kind',
                        'future_access':prediction()}} for i in range(1,4)]}
        file=self.root/'timing.json';file.write_text(json.dumps(timing))
        for mode in ('baseline','materialization'):
            out=self.root/mode
            result=worker(self.path,file,out,mode,skip_idle=True)
            self.assertLess(result['task_wall_seconds'],20)
            self.assertGreaterEqual(result['reconstructed_task_seconds'],240)
            self.assertAlmostEqual(result['reconstructed_task_seconds'],
                result['task_wall_seconds']+result['skipped_idle_seconds'],places=6)
            timeline=json.loads((out/'timeline.json').read_text())
            for i,w in enumerate(timeline['waits']):
                self.assertGreater(w['skipped_idle_ns'],0)
                if mode!='baseline':
                    events=[e for e in timeline['background'] if
                        (e['type']=='worker_ready' if i==0 else e['type']=='decision' and e['step']==i)]
                    self.assertEqual(len(events),1)
                    self.assertLessEqual(events[0]['ended_ns'],w['ended_ns'])
            if mode!='baseline':
                self.assertTrue(timeline['queries'][2]['materializations_used'])

    def test_timing_extractor_preserves_failed_queries_and_relative_gaps(self):
        from agent_db_tool.optimization.timing import extract
        source=self.root/'source';source.mkdir()
        (source/'summary.json').write_text(json.dumps({'answer_submitted':True,'timed_out':False,'model':'fixture'}))
        (source/'task_meta.json').write_text(json.dumps({'database_sha256':'fixture'}))
        (source/'live-launch.json').write_text(json.dumps({'started_at':1000}))
        requests=[];clients=[]
        for step,start,end,status in [(1,1001,1002,'completed'),(2,1005,1006,'error')]:
            args={'sql':'SELECT '+str(step),'future_access':prediction()}
            rid=str(step);requests.append({'record':'request','request_id':rid,'step_id':step,'arguments':args})
            response={'request_id':rid,'status':'ok' if status=='completed' else 'db_error'}
            state={'status':status,'input':args,'time':{'start':start*1000,'end':end*1000},
                   'output' if status=='completed' else 'error':json.dumps(response)}
            clients.append({'type':'tool_use','part':{'tool':'agentdb_db_query','state':state}})
        clients.append({'type':'tool_use','part':{'tool':'agentdb_submit_answer','state':{
            'status':'completed','output':json.dumps({'submitted':True}),'time':{'start':1009000,'end':1010000}}}})
        (source/'events.jsonl').write_text('\n'.join(map(json.dumps,requests))+'\n')
        (source/'agent.jsonl').write_text('\n'.join(map(json.dumps,clients))+'\n')
        result=extract(source,self.root/'extracted.json')
        self.assertEqual([c['gap_before_seconds'] for c in result['calls']],[1,3])
        self.assertEqual(result['final_gap_seconds'],4)
        self.assertEqual(result['total_wait_seconds'],8)
        self.assertEqual(result['calls'][1]['source_status'],'db_error')
        clients[1]['part']['state']['time']['start']=1001500
        (source/'agent.jsonl').write_text('\n'.join(map(json.dumps,clients))+'\n')
        with self.assertRaises(ValueError):extract(source,self.root/'bad.json')

    def test_immediate_stop_cleans_worker(self):
        engine=AsyncEngine(self.path,'combined',DEFAULT_CONFIG)
        engine.submit(1,prediction());engine.submit(2,prediction())
        result=engine.close();self.assertFalse(result['forced_termination']);self.assertEqual(result['exit_code'],0)

    def test_first_object_usable_while_second_build_is_pending(self):
        ctx=mp.get_context('spawn');started=ctx.Event();release=ctx.Event();stop=ctx.Event();events=ctx.Queue()
        proc=ctx.Process(target=held_second_build,args=(str(self.path),started,release,events,stop));proc.start()
        try:
            self.assertTrue(started.wait(8))
            received=[]
            while not any(e['type']=='object_ready' for e in received):received.append(events.get(timeout=2))
            obj=next(e['object'] for e in received if e['type']=='object_ready')
            self.assertLessEqual(obj['commit_return_ns'],obj['ready_ns'])
            sql='SELECT kind,SUM(amount) AS s FROM sales GROUP BY kind'
            changed,used,_=rewrite(sql,[obj],self.db.catalog)
            self.assertEqual(used,[obj['name']]);self.assertTrue(proc.is_alive())
            self.db.begin_snapshot()
            try:
                r=self.db.execute(changed,self.root/'early.jsonl')
                self.assertEqual(r['status'],'ok')
                self.assertEqual(self.db.db.execute(sql).fetchall(),self.db.db.execute(changed).fetchall())
            finally:self.db.end_snapshot()
            self.assertFalse(release.is_set())
        finally:
            release.set();proc.join(8)
            if proc.is_alive():proc.terminate();proc.join()
            events.close()
        self.assertEqual(proc.exitcode,0)
        self.assertEqual(self.db.db.execute("SELECT name FROM sqlite_master WHERE name LIKE 'fad_%'").fetchall(),[])

    def test_stop_after_first_publication_skips_remaining_builds(self):
        stop=mp.get_context('spawn').Event();events=[]
        backend=AsyncBackend(self.path,stop=stop)
        def emit(e):
            events.append(e)
            if e['type']=='object_ready':stop.set()
        controller=AsyncController(backend,'materialization',DEFAULT_CONFIG,emit,stop)
        try:
            controller.observe_fad(1,two_predictions());actions=controller.observe_fad(2,two_predictions())
            self.assertEqual(sum(e['type']=='object_ready' for e in events),1)
            self.assertEqual(sum(e['type']=='build_started' for e in events),1)
            self.assertEqual(actions[1]['status'],'skipped')
            self.assertIn('stopping',actions[1]['reason'])
        finally:controller.cleanup();backend.close()
        self.assertEqual(self.db.db.execute("SELECT name FROM sqlite_master WHERE name LIKE 'fad_%'").fetchall(),[])

    def test_stop_during_create_rolls_back_unpublished_object(self):
        stop=mp.get_context('spawn').Event();events=[]
        backend=AsyncBackend(self.path,stop=stop)
        controller=AsyncController(backend,'materialization',DEFAULT_CONFIG,events.append,stop)
        try:
            controller.observe_fad(1,two_predictions())
            backend.db.connection.set_trace_callback(lambda sql:stop.set() if sql.startswith('CREATE TABLE "fad_m_') else None)
            actions=controller.observe_fad(2,two_predictions())
            self.assertEqual(actions[0]['status'],'rejected_or_failed')
            self.assertIn('interrupted',actions[0]['error'])
            self.assertEqual(actions[1]['status'],'skipped')
            self.assertFalse(any(e['type']=='object_ready' for e in events))
            self.assertEqual(backend.execute('DELETE FROM sales',self.root/'readonly.jsonl')['status'],'error')
        finally:controller.cleanup();backend.close()
        self.assertEqual(self.db.db.execute('SELECT COUNT(*) FROM sales').fetchone()[0],10000)
        self.assertEqual(self.db.db.execute("SELECT name FROM sqlite_master WHERE name LIKE 'fad_%'").fetchall(),[])

if __name__=='__main__':unittest.main()
