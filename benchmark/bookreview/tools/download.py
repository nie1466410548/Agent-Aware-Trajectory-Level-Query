"""Fetch only bookreview at a pinned upstream revision; verify data hashes."""
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REV = 'b24c8f5586121d4d2f8a5a793ebac530858dd1ab'
BASE = f'https://raw.githubusercontent.com/ucbepic/DataAgentBench/{REV}/'

def fetch(path):
    with urllib.request.urlopen(BASE + path, timeout=120) as response:
        return response.read()

manifest = fetch('dataset_manifest.tsv').decode()
paths = ['db_description.txt', 'db_description_withhint.txt', 'db_config.yaml']
paths += [f'query{i}/{f}' for i in range(1, 4)
          for f in ['query.json', 'ground_truth.csv', 'validate.py']]
hashes = {}
for line in manifest.splitlines():
    if line.startswith('query_bookreview/'):
        path, digest, size = line.split('\t')
        paths.append(path.removeprefix('query_bookreview/'))
        hashes[path] = (digest, int(size))
for path in paths:
    full = 'query_bookreview/' + path
    data = fetch(full)
    if data.startswith(b'version https://git-lfs.github.com/spec/v1'):
        url = f'https://media.githubusercontent.com/media/ucbepic/DataAgentBench/{REV}/{full}'
        with urllib.request.urlopen(url, timeout=120) as response:
            data = response.read()
    if full in hashes:
        digest, size = hashes[full]
        if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
            raise RuntimeError(f'Data hash mismatch or LFS pointer: {path}')
    target = ROOT / 'upstream' / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    print(path, len(data), flush=True)
(ROOT / 'upstream' / 'source.json').write_text(json.dumps(
    {'repository': 'https://github.com/ucbepic/DataAgentBench', 'commit': REV,
     'data_hashes': hashes}, indent=2) + '\n')
