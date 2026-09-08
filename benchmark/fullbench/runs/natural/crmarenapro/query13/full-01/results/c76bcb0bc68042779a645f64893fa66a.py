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
start = datetime.date(2022, 6, 25)  # five months before

# Eligible contracts: CompanySignedDate in [start, today]
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
        elig_contracts[clean(c["Id"])] = dt
print("eligible contracts:", len(elig_contracts))

# Eligible opportunities: associated contract is eligible
elig_accts = set()
elig_opps = 0
for o in opps:
    cid = clean(o.get("ContractID__c")) if o.get("ContractID__c") else None
    if cid and cid in elig_contracts:
        elig_opps += 1
        elig_accts.add(clean(o["AccountId"]))
print("eligible opportunities:", elig_opps, "accounts:", len(elig_accts))

# Orders for those accounts
order_amount = {}
order_owner = {}
eligible_order_ids = set()
for o in orders:
    if clean(o["AccountId"]) in elig_accts:
        eligible_order_ids.add(clean(o["Id"]))
        order_owner[clean(o["Id"])] = clean(o["OwnerId"])
print("eligible orders:", len(eligible_order_ids))

for it in items:
    oid = clean(it["OrderId"])
    if oid in eligible_order_ids:
        try:
            amt = float(it["Quantity"]) * float(it["UnitPrice"])
        except Exception:
            continue
        order_amount[oid] = order_amount.get(oid, 0.0) + amt

# Aggregate by owner (agent)
agent_sales = {}
for oid, amt in order_amount.items():
    owner = order_owner.get(oid)
    agent_sales[owner] = agent_sales.get(owner, 0.0) + amt

ranked = sorted(agent_sales.items(), key=lambda x: -x[1])
print("\nTop agents by sales (orders linked to eligible opportunities):")
for a, s in ranked[:10]:
    print(f"{a}: {s:.2f}")
