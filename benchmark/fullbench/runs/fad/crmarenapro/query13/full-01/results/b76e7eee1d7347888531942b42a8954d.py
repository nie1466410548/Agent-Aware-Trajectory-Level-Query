import json, pandas as pd

def load(p):
    with open(p) as f: return pd.DataFrame(json.load(f))

opps = load("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query13/full-01/results/d4ce3a3fba0b48dcbb5b3b819218740f.json")
orders = load("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query13/full-01/results/40119010292543b486fbc63bea393d6c.json")

strip = lambda s: str(s).lstrip('#').strip()
for df, cols in [(opps, ["AccountId","OwnerId"]), (orders, ["AccountId","OwnerId"])]:
    for c in cols: df[c] = df[c].map(strip)

eligible_accounts = set(opps["AccountId"])
print("eligible accounts:", eligible_accounts)

orders["eligible"] = orders["AccountId"].isin(eligible_accounts)
el = orders[orders["eligible"]]
print("\nEligible orders:", len(el))
print(el[["OrderId","AccountId","OwnerId","EffectiveDate","SalesAmount"]].to_string())

print("\n=== By Order OwnerId ===")
g1 = el.groupby("OwnerId")["SalesAmount"].agg(["sum","count"]).sort_values("sum", ascending=False)
print(g1.to_string())

# map account -> opportunity owners
acc2opp = opps.groupby("AccountId")["OwnerId"].apply(list).to_dict()
print("\nacc->opp owners:", acc2opp)
print("\n=== By Opportunity OwnerId (account mapped) ===")
rows=[]
for _, r in el.iterrows():
    for ow in acc2opp[r["AccountId"]]:
        rows.append((ow, r["SalesAmount"]))
g2 = pd.DataFrame(rows, columns=["OwnerId","amt"]).groupby("OwnerId")["amt"].sum().sort_values(ascending=False)
print(g2.to_string())
