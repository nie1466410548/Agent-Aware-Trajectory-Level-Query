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

elig_contracts = {}
for c in contracts:
    d = c.get("CompanySignedDate")
    if not d:
        continue
    try:
        dt = datetime.date.fromisoformat(str(d).strip()[:10])
    except Exception:
        continue
    if start <= dt <= today:
        elig_contracts[clean(c["Id"])] = (dt, clean(c["AccountId"]))

# eligible opportunities with owner & account
elig_opps = []
for o in opps:
    cid = clean(o.get("ContractID__c")) if o.get("ContractID__c") else None
    if cid and cid in elig_contracts:
        elig_opps.append((clean(o["Id"]), clean(o["AccountId"]), clean(o["OwnerId"]), cid))

print("Eligible opportunities detail:")
for oid, acct, own, cid in elig_opps:
    print(f"  opp={oid} acct={acct} owner={own} contract_signed={elig_contracts[cid][0]}")

# order totals
order_total = {}
for it in items:
    oid = clean(it["OrderId"])
    try:
        amt = float(it["Quantity"]) * float(it["UnitPrice"])
    except Exception:
        continue
    order_total[oid] = order_total.get(oid, 0.0) + amt

orders_by_acct = {}
for o in orders:
    orders_by_acct.setdefault(clean(o["AccountId"]), []).append((clean(o["Id"]), clean(o["OwnerId"]), o.get("EffectiveDate")))

# Variant B: attribute order sales to opportunity owner (per eligible opp's account)
agent_salesB = {}
seen_orders = set()
for oid, acct, own, cid in elig_opps:
    for ooid, oown, eff in orders_by_acct.get(acct, []):
        if ooid in seen_orders:
            continue
        seen_orders.add(ooid)
        agent_salesB[own] = agent_salesB.get(own, 0.0) + order_total.get(ooid, 0.0)

print("\nVariant B (attribute to OPPORTUNITY owner):")
for a, s in sorted(agent_salesB.items(), key=lambda x: -x[1])[:5]:
    print(f"  {a}: {s:.2f}")

# Variant A recap (order owner)
elig_accts = set(a for _, a, _, _ in elig_opps)
agent_salesA = {}
for o in orders:
    if clean(o["AccountId"]) in elig_accts:
        ooid = clean(o["Id"])
        own = clean(o["OwnerId"])
        agent_salesA[own] = agent_salesA.get(own, 0.0) + order_total.get(ooid, 0.0)
print("\nVariant A (attribute to ORDER owner):")
for a, s in sorted(agent_salesA.items(), key=lambda x: -x[1])[:5]:
    print(f"  {a}: {s:.2f}")
