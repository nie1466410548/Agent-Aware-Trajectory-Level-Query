"""Portable reading copies. Original agent answers and figures remain unchanged."""
import os,re,json
from pathlib import Path
from urllib.parse import unquote
from common import dump,sha

def render_answer(run,target):
 original=run/'answer.md'
 if not original.exists(): return None
 target.parent.mkdir(parents=True,exist_ok=True);changes=[];missing=[]
 def replace(match):
  raw=match.group(2);url=raw.strip().strip('<>')
  if url.startswith(('http:','https:','data:','mailto:','#')):return match.group(0)
  path=Path(unquote(url.split('#',1)[0]));candidates=[]
  if url.startswith('/work/'):candidates.append(run/'work'/url[len('/work/'):])
  if not path.is_absolute():candidates.extend([run/'work'/path,run/path])
  elif path.is_relative_to(run):candidates.append(path)
  source=next((p.resolve() for p in candidates if p.exists() and p.resolve().is_relative_to(run.resolve())),None)
  if source is None:missing.append(url);return match.group(0)
  rewritten=os.path.relpath(source,target.parent)
  if '#' in url:rewritten+='#'+url.split('#',1)[1]
  changes.append({'original':url,'rewritten':rewritten,'file_sha256':sha(source) if source.is_file() else None})
  return match.group(1)+'<'+rewritten+'>'+match.group(3)
 content=re.sub(r'(!?\[[^\]]*\]\()([^\n)]+)(\))',replace,original.read_text())
 header='<!-- Reading copy: local artifact links normalized. Original answer is preserved at '+os.path.relpath(original,target.parent)+' -->\n\n'
 target.write_text(header+content)
 dump(target.with_suffix('.links.json'),{'original_sha256':sha(original),'reading_copy_sha256':sha(target),'path_rewrites':changes,'unresolved_original_links':missing,'content_policy':'Only local Markdown link targets changed; no answer claims edited.'})
 return target
