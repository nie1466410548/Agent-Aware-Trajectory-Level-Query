"""One independent main attempt, with batch-wide provider failure latch."""
import argparse, fcntl, json, time
from common import *
import run as runner
from proxy import Relay

class BatchRelay(Relay):
    stop_path=ROOT/'state/parallel-stop.json'
    @property
    def stopped(self):
        if self._local_stop is None and self.stop_path.exists():
            event=json.loads(self.stop_path.read_text())
            self._local_stop={**event,'propagated':event.get('task_id')!=self.run.parent.name}
            dump(self.run/'provider/stop.json',self._local_stop)
        return self._local_stop
    @stopped.setter
    def stopped(self,value): self._local_stop=value
    def fail(self,event):
        with self.stop_path.with_suffix('.lock').open('a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            if not self.stop_path.exists():
                dump(self.stop_path,{**event,'task_id':self.run.parent.name,'time':time.time()})
            if self._local_stop is None:
                self._local_stop={**json.loads(self.stop_path.read_text()),'propagated':json.loads(self.stop_path.read_text()).get('task_id')!=self.run.parent.name}
                dump(self.run/'provider/stop.json',self._local_stop)

def main():
    p=argparse.ArgumentParser();p.add_argument('task_id');p.add_argument('--concurrency',type=int,required=True);args=p.parse_args()
    assert not BatchRelay.stop_path.exists(),'Batch already stopped'
    runner.Relay=BatchRelay
    runner.CONFIG={**runner.CONFIG,'concurrency':args.concurrency,'scheduler':'parallel_v1','timing_context':'Concurrent independent tasks; original query timings may include resource contention.'}
    entry=next(e for e in records(ROOT/'manifests/tasks.jsonl') if e['task_id']==args.task_id)
    summary=runner.run_task(args.task_id,entry)
    print(json.dumps({'task_id':args.task_id,'status':summary['status'],'all_sql_attempts':summary['all_sql_attempts']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
