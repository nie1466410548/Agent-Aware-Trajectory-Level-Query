import json, collections

rows = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query8/full-01/results/475b9e44709c4b199411ad7a8ee40cdc.json"))

transfers = [r for r in rows if r["oldvalue__c"] is not None]
transfers.sort(key=lambda r: r["createddate"])
print("total transfers:", len(transfers))
for r in transfers:
    print(r["createddate"], r["oldvalue__c"], "->", r["newvalue__c"], r["caseid__c"])

# per-agent transfer counts in rolling window
lo, hi = "2022-04-10", "2023-04-10"
cnt = collections.Counter(r["oldvalue__c"] for r in transfers if lo <= r["createddate"][:10] < hi)
print("\nwindow transfer counts:", dict(cnt))

# handled cases (all time) for these agents
handled = collections.Counter(r["newvalue__c"] for r in rows)
for a in cnt:
    print(a, "handled(all time):", handled[a])
