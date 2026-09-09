"""Refresh delivery hashes/reading links after documentation-only additions."""
import hashlib,json,re,time
from common import *

def main():
 sources=sorted((ROOT/'tools').glob('*.py'));version=hashlib.sha256(''.join(sha(p) for p in sources).encode()).hexdigest();target=REPORT/'code_versions'/version;target.mkdir(parents=True,exist_ok=True)
 for p in sources:(target/p.name).write_bytes(p.read_bytes())
 dump(target/'manifest.json',{'phase':'delivery_index_refresh','version':version,'files':{p.name:sha(p) for p in sources}})
 broken=[]
 for path in REPORT.rglob('*.md'):
  for match in re.finditer(r'!?\[[^\]]*\]\(([^\n)]+)\)',path.read_text()):
   link=match.group(1).strip().strip('<>')
   if link.startswith(('http:','https:','mailto:','data:','#')):continue
   dest=link.split('#')[0]
   if dest and not (path.parent/dest).exists():broken.append({'file':str(path.relative_to(REPORT)),'link':link})
 dump(REPORT/'link_audit.json',{'broken_local_links':broken,'scope':'Generated workload reports and normalized answer copies; raw agent answers preserved separately.'})
 files=[]
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file() or p.is_relative_to(ROOT/'runtime') or '__pycache__' in p.parts or p.suffix in ['.part','.pyc'] or p.name=='evidence_index.json':continue
  files.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)})
 dump(REPORT/'evidence_index.json',{'generated_at':time.time(),'files':files,'databases':'Original databases are separately verified by manifests/remote-hash-check.json and per-task post-run hashes; downloaded DBs excluded from this index.'})
 print(json.dumps({'files':len(files),'bytes':sum(p['bytes'] for p in files),'broken_links':broken}))
if __name__=='__main__':main()
