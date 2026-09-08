import json, re

base = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query2/full-01/results/"
pinfo = json.load(open(base + "1f6029e33ba144eca49e5cb3265045e7.json"))

def parse_name(text):
    m = re.search(r"under the name ([\w.\-]+/[\w.\-]+)", text)
    if m: return m.group(1)
    m = re.search(r"named ([\w.\-]+/[\w.\-]+)", text)
    if m: return m.group(1)
    m = re.search(r"project ([\w.\-]+/[\w.\-]+)", text)
    if m: return m.group(1)
    return None

def parse_forks(text):
    for p in [r"([\d,]+)\s+forks\b", r"forks count of ([\d,]+)", r"forked ([\d,]+) times", r"has ([\d,]+) fork\b", r"and ([\d,]+) fork\b"]:
        m = re.search(p, text)
        if m:
            return int(m.group(1).replace(",", ""))
    return None

for r in pinfo:
    t = r["Project_Information"]
    if parse_name(t) is None or parse_forks(t) is None:
        print("UNPARSED:", t)
