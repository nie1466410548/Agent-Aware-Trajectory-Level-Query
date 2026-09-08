import json, re

RUN = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PATENTS/query3/full-01/"

with open(RUN + "uc_pubs.json") as f:
    uc_pubs = set(json.load(f))

with open(RUN + "results/3fb80f9246db4c4dac09758775f4433a.json") as f:
    rows = json.load(f)

print("rows:", len(rows))

def get_assignee(info):
    # patterns: "X holds the", "assigned to X", "owned by X", "held by X", "belonging to X"
    m = re.match(r"^(.+?) holds the ", info)
    if m: return m.group(1)
    for pat in [r"assigned to (.+?) and has", r"owned by (.+?) and has", r"held by (.+?) and has",
                r"belonging to (.+?) and has", r"assigned to (.+?), with", r"owned by (.+?), with",
                r"held by (.+?), with", r"belonging to (.+?), with"]:
        m = re.search(pat, info)
        if m: return m.group(1)
    return None

results = []
for r in rows:
    info = r["Patents_info"]
    assignee = get_assignee(info)
    pubs = re.findall(r"\b([A-Z]{2}-[A-Z0-9]+-[A-Z0-9]+)\b", info)
    own_pub = pubs[-1] if pubs else None
    cit = json.loads(r["citation"])
    cited_uc = sorted({c["publication_number"] for c in cit if c.get("publication_number") in uc_pubs})
    cpc = json.loads(r["cpc"])
    primary = sorted({c["code"] for c in cpc if c.get("first")})
    subclasses = sorted({c[:4] for c in primary})
    results.append({"assignee": assignee, "own_pub": own_pub, "cited_uc": cited_uc,
                    "primary_codes": primary, "subclasses": subclasses})
    print(json.dumps(results[-1], indent=1))

# exclude UNIV CALIFORNIA itself
final = [r for r in results if r["assignee"] and "UNIV CALIFORNIA" not in r["assignee"].upper()]
print("\nExcluding UC itself:", len(final))
with open(RUN + "citing_analysis.json", "w") as f:
    json.dump(final, f, indent=1)

all_subs = sorted({s for r in final for s in r["subclasses"]})
print("subclasses needed:", all_subs)
