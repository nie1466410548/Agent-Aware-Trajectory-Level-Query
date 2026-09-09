"""Verify local files against fixed-revision HF LFS SHA256 / Git blob SHA1."""
import hashlib,json
from common import *
def main():
 remote={r['path']:r for r in json.loads((ROOT/'manifests/remote-files.json').read_text()) if r['path'].endswith('.sqlite')};checks=[]
 for row in records(ROOT/'manifests/tasks.jsonl'):
  tid=row['task_id']; r=remote[f'{tid}/{tid}.sqlite']; p=BENCH/'upstream'/tid/f'{tid}.sqlite'; local=None
  if p.exists():
   if 'lfs' in r: local=sha(p)
   else:
    h=hashlib.sha1(f'blob {p.stat().st_size}\0'.encode())
    with p.open('rb') as f:
     for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    local=h.hexdigest()
  expected=r.get('lfs',{}).get('oid',r['oid']);checks.append({'task_id':tid,'algorithm':'sha256' if 'lfs' in r else 'git_blob_sha1','local_hash':local,'remote_hash':expected,'matches':local==expected,'size_matches':p.exists() and p.stat().st_size==r['size']})
 dump(ROOT/'manifests/remote-hash-check.json',checks);print('Verified',sum(c['matches'] and c['size_matches'] for c in checks),'/',len(checks))
 if not all(c['matches'] and c['size_matches'] for c in checks):raise SystemExit(1)
if __name__=='__main__':main()
