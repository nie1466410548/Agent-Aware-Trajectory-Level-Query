"""Verify pinned source blobs and manifest-sized data without reading credentials."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 manifest=json.loads((ROOT/'tasks.json').read_text());tree={x['path']:x for x in json.loads((ROOT/'reports/upstream-tree.json').read_text())['tree'] if x['type']=='blob'}
 paths=set(json.loads((ROOT/'reports/preparation.json').read_text())['files'])
 paths|={p for p in tree if p.startswith('common_scaffold/validate/')}
 result=[];issues=[]
 for name in sorted(paths):
  p=ROOT/'upstream'/name
  if not p.exists():issues.append({'path':name,'error':'missing'});continue
  size=p.stat().st_size;h256=hashlib.sha256();h1=hashlib.sha1();h1.update(f'blob {size}\0'.encode())
  with p.open('rb') as f:
   for chunk in iter(lambda:f.read(8*1024*1024),b''):h256.update(chunk);h1.update(chunk)
  expected=manifest['hashes'].get(name)
  if expected:
   ok=h256.hexdigest()==expected[0] and size==expected[1];method='manifest_sha256_and_size'
  else:
   ok=name in tree and h1.hexdigest()==tree[name]['sha'];method='pinned_git_blob_sha1'
  result.append({'path':name,'bytes':size,'sha256':h256.hexdigest(),'method':method,'verified':ok})
  if not ok:issues.append({'path':name,'error':'hash mismatch'})
 out={'commit':manifest['commit'],'verified_files':sum(x['verified'] for x in result),'files':result,'issues':issues}
 (ROOT/'reports/source-integrity.json').write_text(json.dumps(out,indent=2)+'\n')
 print('Source verified',out['verified_files'],'/',len(result),'issues',len(issues))
 if issues:print(json.dumps(issues,indent=2))
if __name__=='__main__':main()
