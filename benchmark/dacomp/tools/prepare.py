"""Fetch the four selected DAComp tasks without invoking an agent or evaluator."""
import hashlib
import json
from pathlib import Path
import sqlite3
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
REPO = "DAComp/dacomp-da"
REVISION = "2cc22149cdfe16cec41851ccae791c2d2c873bb3"
TASKS = ["dacomp-006", "dacomp-003", "dacomp-004", "dacomp-005"]
BASE = f"https://huggingface.co/datasets/{REPO}/resolve/{REVISION}"


def fetch(path):
    with urlopen(f"{BASE}/{path}", timeout=120) as response:
        return response.read()


def main():
    source = fetch("dacomp-da.jsonl")
    records = {r["instance_id"]: r for r in map(json.loads, source.splitlines())}
    manifest = {"repository": REPO, "revision": REVISION,
                "task_file_sha256": hashlib.sha256(source).hexdigest(),
                "agent_runs_at_preparation": 0, "tasks": []}
    for task in TASKS:
        directory = ROOT / "upstream" / task
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{task}.sqlite"
        if not path.exists():
            temporary = path.with_suffix(".sqlite.download")
            temporary.write_bytes(fetch(f"{task}/{task}.sqlite"))
            temporary.replace(path)
        raw = path.read_bytes()
        with sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True) as db:
            integrity = db.execute("PRAGMA quick_check").fetchall()
            if integrity != [("ok",)]:
                raise RuntimeError(f"{task}: database integrity check failed")
            tables = []
            for name, ddl in db.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall():
                quoted = '"' + name.replace('"', '""') + '"'
                tables.append({"name": name, "ddl": ddl,
                               "rows": db.execute(f"SELECT COUNT(*) FROM {quoted}").fetchone()[0],
                               "columns": [r[1] for r in db.execute(f"PRAGMA table_info({quoted})")]})
        (directory / "task.json").write_text(json.dumps(records[task], indent=2, ensure_ascii=False) + "\n")
        (directory / "schema.json").write_text(json.dumps(tables, indent=2, ensure_ascii=False) + "\n")
        manifest["tasks"].append({"task_id": task, "database_bytes": len(raw),
                                  "database_sha256": hashlib.sha256(raw).hexdigest(),
                                  "quick_check": "ok", "tables": tables})
        print(f"{task}: {len(raw):,} bytes, {len(tables)} tables, {sum(t['rows'] for t in tables):,} rows")
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
