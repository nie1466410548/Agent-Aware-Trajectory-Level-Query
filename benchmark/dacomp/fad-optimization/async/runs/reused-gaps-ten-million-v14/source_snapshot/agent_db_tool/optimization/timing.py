"""Extract one real client's relative SQL gaps, including final report generation."""
import json
from pathlib import Path
from .replay import sha


def extract(run,output):
    run=Path(run)
    summary=json.loads((run/'summary.json').read_text())
    if not summary['answer_submitted'] or summary['timed_out'] or summary.get('incomplete_requests',0):raise ValueError('source task incomplete')
    events=[json.loads(l) for l in (run/'events.jsonl').read_text().splitlines()]
    requests={e['request_id']:e for e in events if e['record']=='request'}
    completions={e['request_id']:e for e in events if e['record']=='completion'}
    clients=[json.loads(l) for l in (run/'agent.jsonl').read_text().splitlines()]
    calls=[];answer=None
    for event in clients:
        if event.get('type')!='tool_use':continue
        part=event['part'];state=part.get('state',{});timing=state.get('time',{})
        if part['tool']=='agentdb_submit_answer':
            if state.get('status')=='completed':
                submitted=json.loads(state['output']) if isinstance(state.get('output'),str) else state.get('output',{})
                if submitted.get('submitted') is True:answer=timing['end']/1000
        if part['tool']!='agentdb_db_query':continue
        if state.get('status') not in ('completed','error'):raise ValueError('incomplete SQL call')
        raw=state.get('output') if state.get('status')=='completed' else state.get('error');response=json.loads(raw) if isinstance(raw,str) else raw
        request=requests[response['request_id']]
        if state['input']!=request['arguments']:raise ValueError('client/server argument mismatch')
        calls.append({'step':request['step_id'],'request_id':request['request_id'],
                      'arguments':request['arguments'],'client_start':timing['start']/1000,
                      'client_end':timing['end']/1000,'source_status':response['status']})
    calls.sort(key=lambda c:c['client_start'])
    if len(calls)!=len(requests) or not calls or answer is None:raise ValueError('missing calls or report timing')
    queued=any(c['client_start']<p['client_end'] for p,c in zip(calls,calls[1:]))
    if queued:
        # MCP serves requests serially even when the Agent dispatches several
        # tools together. Use observed service boundaries, never turn time in
        # the queue into idle time available to the background optimizer.
        calls.sort(key=lambda c:requests[c['request_id']]['time'])
        for call in calls:
            call['service_start']=requests[call['request_id']]['time']
            call['service_end']=completions[call['request_id']]['time']
            if not (call['client_start']<=call['service_start']<=call['service_end']<=call['client_end']+.001):
                raise ValueError('service timestamps outside client call')
    launch=json.loads((run/'live-launch.json').read_text())['started_at']
    previous=launch
    for call in calls:
        gap=call.get('service_start',call['client_start'])-previous
        if gap<0 or call['client_end']<call['client_start']:raise ValueError('overlap or inconsistent timestamps')
        call['gap_before_seconds']=gap
        previous=call.get('service_end',call['client_end'])
    final=answer-previous
    if final<0:raise ValueError('report precedes final query completion')
    meta=json.loads((run/'task_meta.json').read_text())
    result={'source_run':str(run.resolve()),'source_database_sha256':meta['database_sha256'],
            'source_events_sha256':sha(run/'events.jsonl'),'source_client_sha256':sha(run/'agent.jsonl'),
            'model':summary['model'],'calls':calls,'final_gap_seconds':final,
            'total_wait_seconds':sum(c['gap_before_seconds'] for c in calls)+final,
            'source_task_to_report_seconds':answer-launch,
            'has_queued_client_calls':queued,
            'timing_basis':'serial_mcp_service' if queued else 'client_tool',
            'timing_note':('Serial MCP service start/end boundaries from request/completion logs; original overlapping client timestamps retained. Queue residence is not an idle optimization window. Measures sequential database service, not sum of overlapping client call durations.' if queued else 'Client tool start/end timestamps; gaps include model, other tool and client work. No compression.')}
    Path(output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result
