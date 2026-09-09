"""Credential-in-memory provider relay. One upstream request per client request;
latch on first HTTP/network error, preventing any paid upstream retry.
Only request bodies, safe response headers and raw response bodies are archived.
"""
import http.server, json, threading, time, urllib.request, urllib.error
from common import *
class Relay:
 def __init__(self,run,provider):
    self.run=run; self.provider=provider; self.lock=threading.Lock(); self.stopped=None; self.count=0
    (run/'provider').mkdir(exist_ok=True)
    relay=self
    class Handler(http.server.BaseHTTPRequestHandler):
      def log_message(self,*a): pass
      def do_POST(self):
        with relay.lock:
          relay.count+=1; rid=f'R{relay.count}'; body=self.rfile.read(int(self.headers.get('Content-Length','0')))
          (run/'provider'/f'{rid}.request.json').write_bytes(body)
          if relay.stopped:
            append(run/'provider/requests.jsonl',{'id':rid,'status':'blocked_local_retry','time':time.time()})
            self.send_response(400); self.end_headers(); self.wfile.write(b'{"error":{"message":"Run stopped after provider failure; no upstream retry"}}'); return
          opts=provider['options']; url=opts['baseURL'].rstrip('/')+self.path
          req=urllib.request.Request(url,data=body,headers={'Authorization':'Bearer '+opts['apiKey'],'Content-Type':'application/json','Accept':self.headers.get('Accept','application/json')},method='POST')
          event={'id':rid,'start_time':time.time(),'path':self.path}
          try:
            response=urllib.request.urlopen(req,timeout=180)
          except urllib.error.HTTPError as e: response=e
          except Exception as e:
            relay.fail({'id':rid,'kind':'service_error','error':repr(e)}); self.send_response(400); self.end_headers(); return
          status=response.status; event['http_status']=status
          safe={k:v for k,v in response.headers.items() if k.lower() in ['content-type','date','retry-after','x-request-id','request-id']}; event['headers']=safe
          if status>=400:
            raw=response.read(); (run/'provider'/f'{rid}.response.raw').write_bytes(raw)
            msg=raw.decode(errors='replace'); lower=msg.lower()
            quota=any(s in lower for s in ['insufficient','quota','credit','balance','余额','额度','欠费','resource_exhausted','usage limit'])
            relay.fail({'id':rid,'kind':'quota_interrupted' if quota else 'service_error','http_status':status,'error':msg})
            # 400 removes HTTP-status based retry; latch is authoritative regardless.
            self.send_response(400); self.send_header('Content-Type','application/json'); self.end_headers()
            try: self.wfile.write(raw)
            except BrokenPipeError: pass
          else:
            self.send_response(status); self.send_header('Content-Type',response.headers.get('Content-Type','application/json')); self.end_headers()
            try:
              with (run/'provider'/f'{rid}.response.raw').open('wb') as f:
                buffer=b''
                while chunk:=response.read1(65536):
                  f.write(chunk); f.flush(); self.wfile.write(chunk); self.wfile.flush(); buffer+=chunk
                  while b'\n' in buffer:
                    line,buffer=buffer.split(b'\n',1)
                    if line.startswith(b'data: '): line=line[6:]
                    try: message=json.loads(line)
                    except (ValueError,UnicodeDecodeError): continue
                    if isinstance(message,dict) and message.get('error'):
                      msg=json.dumps(message,ensure_ascii=False); low=msg.lower()
                      quota=any(s in low for s in ['insufficient','quota','credit','balance','余额','额度'])
                      relay.fail({'id':rid,'kind':'quota_interrupted' if quota else 'service_error','http_status':status,'error':msg})
            except Exception as e: relay.fail({'id':rid,'kind':'service_error','error':repr(e)})
          response.close(); event['end_time']=time.time(); append(run/'provider/requests.jsonl',event)
    self.server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    self.thread=threading.Thread(target=self.server.serve_forever,daemon=True); self.thread.start()
 def fail(self,event):
    self.stopped=event; dump(self.run/'provider/stop.json',event)
 def close(self): self.server.shutdown(); self.server.server_close()
 @property
 def base_url(self): return f'http://127.0.0.1:{self.server.server_port}'
