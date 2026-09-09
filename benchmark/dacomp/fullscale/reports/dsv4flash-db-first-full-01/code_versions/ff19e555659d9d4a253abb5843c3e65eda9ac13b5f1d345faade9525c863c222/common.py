import hashlib, json, os, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT.parent
BATCH = 'dsv4flash-db-first-full-01'
REVISION = '2cc22149cdfe16cec41851ccae791c2d2c873bb3'
MODEL = 'glm-custom/DeepSeek-V4-Flash-0731'
PYTHON = BENCH / '.venv/bin/python'
REPORT = ROOT / 'reports' / BATCH

def dump(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix+'.part')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n'); tmp.replace(path)

def append(path, data):
    with Path(path).open('a') as f:
        f.write(json.dumps(data, ensure_ascii=False, default=str)+'\n'); f.flush(); os.fsync(f.fileno())

def records(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()] if Path(path).exists() else []

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()
