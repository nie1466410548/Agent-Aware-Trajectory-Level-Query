import json, collections

rows = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query8/full-01/results/475b9e44709c4b199411ad7a8ee40cdc.json"))

today = "2023-04-10"

windows = {
    "rolling_12m": ("2022-04-10", "2023-04-10"),
    "cal_4q": ("2022-04-01", "2023-04-01"),
    "cal_4q_inclQ2start": ("2022-04-01", "2023-04-10"),
}

# handled cases per agent (all time): agents appear as newvalue (initial or transfer target)
handled = collections.Counter()
for r in rows:
    handled[r["newvalue__c"]] += 1

print("agents handling >0 cases:", len(handled))

for name,(lo,hi) in windows.items():
    trans = collections.Counter()
    for r in rows:
        d = r["createddate"][:10]
        if r["oldvalue__c"] is not None and lo <= d < hi:
            trans[r["oldvalue__c"]] += 1
    # all agents who handled >0 cases; transfer count defaults to 0
    cands = [(a, trans.get(a,0)) for a in handled]
    cands.sort(key=lambda x:(x[1],x[0]))
    print("\nwindow", name, lo, hi)
    print("total transfer events in window:", sum(trans.values()))
    for a,c in cands[:12]:
        print(a, c, "handled:", handled[a])
