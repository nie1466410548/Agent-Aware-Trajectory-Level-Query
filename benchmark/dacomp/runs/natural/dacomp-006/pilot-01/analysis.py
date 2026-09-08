import json, pandas as pd, numpy as np

R = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/dacomp/runs/natural/dacomp-006/pilot-01/results/"

region_m = pd.DataFrame(json.load(open(R+"bbba0500d8ae439d9f4206db9bcd65b0.json")))
sc = pd.DataFrame(json.load(open(R+"dba21aaa488a4a50844a2225fa3f465e.json")))
sc_prod = pd.DataFrame(json.load(open(R+"91c3b0c7572b44eb898eca77acc81baf.json")))

# 1. Volatility comparison across regions
g = region_m.groupby("region")["profit"].agg(["mean","std","min","max"])
g["cv_pct"] = g["std"]/g["mean"]*100
g["max_min_ratio"] = g["max"]/g["min"]
# mean absolute MoM % change
mom = region_m.sort_values(["region","month"]).groupby("region")["profit"].apply(lambda s: s.pct_change().abs().mean()*100)
g["mean_abs_mom_pct"] = mom
print("=== Regional monthly-profit volatility ===")
print(g.round(2).to_string())

# 2. South China monthly decomposition
sc = sc.sort_values("month").reset_index(drop=True)
print("\n=== South China monthly ===")
sc["avg_rev_per_order"] = sc["revenue"]/sc["orders"]
sc["cost_ratio"] = sc["cost"]/sc["revenue"]
sc["profit_mom"] = sc["profit"].pct_change()*100
print(sc[["month","orders","qty","revenue","cost","profit","avg_rev_per_order","cost_ratio","profit_mom"]].round(3).to_string())

# correlations with profit
cols = ["orders","qty","list_rev","vas_rev","discount","freight","warehousing","other_cost","cost"]
print("\n=== Correlation of components with monthly profit (SC) ===")
print(sc[["profit"]+cols].corr()["profit"].round(3).to_string())

# Decompose profit variance: profit = revenue - cost; revenue = orders * avg_rev
# Contribution of each component to MoM profit change
d = sc.set_index("month").diff()
d["d_rev"] = d["revenue"]; d["d_cost"] = d["cost"]
print("\n=== MoM deltas (SC) ===")
print(d[["profit","revenue","cost","orders"]].round(1).to_string())
# share of variance explained: var(revenue) vs var(cost) vs cov
v = sc[["revenue","cost","profit"]].var()
cov_rc = sc["revenue"].cov(sc["cost"])
print("\nVar(profit)=%.0f  Var(rev)=%.0f  Var(cost)=%.0f  2Cov=%.0f" % (v["profit"], v["revenue"], v["cost"], 2*cov_rc))
print("Revenue share of profit variance: %.1f%%" % ((v["revenue"]-2*cov_rc)/v["profit"]*100))

# 3. Product-level contribution to SC monthly profit variance
piv = sc_prod.pivot_table(index="month", columns="product", values="profit", aggfunc="sum").fillna(0)
piv = piv.sort_index()
total = piv.sum(axis=1)
print("\n=== Per-product CV of monthly profit (SC) ===")
prod_cv = (piv.std()/piv.mean()*100).sort_values(ascending=False)
print(prod_cv.round(1).to_string())
# variance contribution: cov of each product series with total / var(total)
vt = total.var()
contrib = {c: piv[c].cov(total)/vt*100 for c in piv.columns}
print("\n=== Product contribution to total monthly profit variance (SC) ===")
print(pd.Series(contrib).sort_values(ascending=False).round(1).to_string())

# 4. Loss orders by product
print("\n=== Loss orders by product (SC, full year) ===")
lo = sc_prod.groupby("product").agg(orders=("orders","sum"), neg=("neg_orders","sum"), neg_sum=("neg_profit_sum","sum"))
lo["neg_rate"] = lo["neg"]/lo["orders"]*100
print(lo.sort_values("neg_rate", ascending=False).round(2).to_string())
