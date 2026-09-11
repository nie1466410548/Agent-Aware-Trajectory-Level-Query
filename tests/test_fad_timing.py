import json
import tempfile
import unittest
from pathlib import Path
from agent_db_tool.optimization.timing import extract


class TimingTest(unittest.TestCase):
    def fixture(self, root, overlap=True):
        def write(name, value):
            (root/name).write_text(json.dumps(value))
        write('summary.json', {'answer_submitted': True, 'timed_out': False, 'model': 'test'})
        write('live-launch.json', {'started_at': 1})
        write('task_meta.json', {'database_sha256': 'test'})
        events=[]; clients=[]
        for step, start, service, end in [(1,2,2.01,4),(2,3 if overlap else 5,4.01 if overlap else 5.01,6)]:
            args={'sql':'SELECT 1'}; rid=str(step)
            events.extend([{'record':'request','request_id':rid,'step_id':step,'time':service,'arguments':args},
                           {'record':'completion','request_id':rid,'time':end-.01}])
            clients.append({'type':'tool_use','part':{'tool':'agentdb_db_query','state':{
                'status':'completed','input':args,'output':{'request_id':rid,'status':'ok'},
                'time':{'start':start*1000,'end':end*1000}}}})
        clients.append({'type':'tool_use','part':{'tool':'agentdb_submit_answer','state':{
            'status':'completed','output':{'submitted':True},'time':{'end':8000}}}})
        (root/'events.jsonl').write_text('\n'.join(map(json.dumps,events)))
        (root/'agent.jsonl').write_text('\n'.join(map(json.dumps,clients)))

    def test_queued_calls_use_serial_service_without_fake_idle(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root)
            t=extract(root,root/'timing.json')
            self.assertEqual(t['timing_basis'],'serial_mcp_service')
            self.assertAlmostEqual(t['calls'][1]['gap_before_seconds'],.02)
            self.assertEqual(t['calls'][1]['client_start'],3)
            self.assertAlmostEqual(t['total_wait_seconds']+sum(c['service_end']-c['service_start'] for c in t['calls']),7)

    def test_nonoverlapping_calls_keep_existing_client_timing(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root,False)
            t=extract(root,root/'timing.json')
            self.assertEqual(t['timing_basis'],'client_tool')
            self.assertEqual([c['gap_before_seconds'] for c in t['calls']],[1,1])

    def test_overlapping_service_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root)
            p=root/'events.jsonl';es=[json.loads(l) for l in p.read_text().splitlines()]
            es[2]['time']=3.5;p.write_text('\n'.join(map(json.dumps,es)))
            with self.assertRaisesRegex(ValueError,'overlap'):extract(root,root/'timing.json')
