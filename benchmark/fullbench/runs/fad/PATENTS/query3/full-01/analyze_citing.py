import json, re

res = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PATENTS/query3/full-01/results/6d77384719b04827a849ef9d3133249b.json"))
uc_pubs = set(json.load(open("uc_pubnums.json")))
print("citing rows:", len(res))

def extract_assignee(info):
    # patterns: "X holds the ...", "... is assigned to X and ...", "owned by X", "held by X", "belonging to X", "assigned to X, with"
    m = re.match(r'^(.+?) holds the ', info)
    if m: return m.group(1)
    for verb in ["assigned to", "owned by", "held by", "belonging to"]:
        m = re.search(verb + r' (.+?) (?:and has|, with|and has pub)', info)
        if m: return m.group(1)
    return "?? " + info

for r in res:
    info = r["Patents_info"]
    assignee = extract_assignee(info)
    cit = json.loads(r["citation"])
    cited_nums = [c.get("publication_number","") for c in cit]
    hits = sorted(set(cited_nums) & uc_pubs)
    cpc = json.loads(r["cpc"])
    first_codes = []
    for c in cpc:
        if c.get("first") and c["code"] not in first_codes:
            first_codes.append(c["code"])
    first_listed = cpc[0]["code"] if cpc else None
    subclasses_first_flag = sorted(set(code[:4] for code in first_codes))
    print("="*80)
    print("ASSIGNEE:", assignee)
    print("PUB row:", info)
    print("cited UC pubs:", hits)
    print("first=true codes:", first_codes)
    print("subclasses(first=true):", subclasses_first_flag)
    print("first listed code:", first_listed)
