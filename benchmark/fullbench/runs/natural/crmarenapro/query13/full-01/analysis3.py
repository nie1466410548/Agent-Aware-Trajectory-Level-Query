import json, datetime

def load(path):
    with open(path) as f:
        return json.load(f)

def clean(v):
    if isinstance(v, str):
        return v.strip().lstrip('#').strip()
    return v

base = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query13/full-01/results/"
contracts = load(base + "15ccccaf775048fe8aec99fc1c468940.json")
opps = load(base + "a7d518c28e224d13aaa6e744baf69692.json")
orders = load(base + "657057162fa44e5da4334753f499309b.json")
items = load(base + "d6ca8c55bb48440f99f4bb46847b5b50.json")

today = datetime.date(2022, 11, 25)
start = datetime.date(2022, 6, 25)

elig_contracts = set()
for c in contracts:
    d = c.get("CompanySignedDate")
    if not d:
        continue
    try:
        dt = datetime.date.fromisoformat(str(d).strip()[:10])
    except Exception:
        continue
    if start <= dt <= today:
        elig_contracts.add(clean(c["Id"]))

elig_accts = set()
for o in opps:
    cid = clean(o.get("ContractID__c")) if o.get("ContractID__c") else None
    if cid and cid in elig_contracts:
        elig_accts.add(clean(o["AccountId"]))

order_total = {}
for it in items:
    oid = clean(it["OrderId"])
    try:
        amt = float(it["Quantity"]) * float(it["UnitPrice"])
    except Exception:
        continue
    order_total[oid] = order_total.get(oid, 0.0) + amt

# Variant A + order EffectiveDate also within past five months
agent_sales = {}
for o in orders:
    if clean(o["AccountId"]) not in elig_accts:
        continue
    eff = o.get("EffectiveDate")
    try:
        effd = datetime.date.fromisoformat(str(eff).strip()[:10])
    except Exception:
        continue
    if not (start <= effd <= today):
        continue
    own = clean(o["OwnerId"])
    agent_sales[own] = agent_sales.get(own, 0.0) + order_total.get(clean(o["Id"]), 0.0)

print("Variant A + EffectiveDate in window:")
for a, s in sorted(agent_sales.items(), key=lambda x: -x[1])[:5]:
    print(f"  {a}: {s:.2f}")

# Variant A, excluding rows whose raw Ids are '#' corrupted on the Order row itself
agent_sales2 = {}
for o in orders:
    if str(o["Id"]).startswith('#') or str(o["OwnerId"]).startswith('#') or str(o["AccountId"]).startswith('#'):
        continue
    if clean(o["AccountId"]) not in elig_accts:
        continue
    own = clean(o["OwnerId"])
    agent_sales2[own] = agent_sales2.get(own, 0.0) + order_total.get(clean(o["Id"]), 0.0)
print("Variant A, clean-rows-only:")
for a, s in sorted(agent_sales2.items(), key=lambda x: -x[1])[:5]:
    print(f"  {a}: {s:.2f}")
