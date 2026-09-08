import json, pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/dacomp/runs/natural/dacomp-006/pilot-01/results/"
region_m = pd.DataFrame(json.load(open(R+"bbba0500d8ae439d9f4206db9bcd65b0.json")))
sc = pd.DataFrame(json.load(open(R+"dba21aaa488a4a50844a2225fa3f465e.json"))).sort_values("month").reset_index(drop=True)
sc_prod = pd.DataFrame(json.load(open(R+"91c3b0c7572b44eb898eca77acc81baf.json")))
sc_prov = pd.DataFrame(json.load(open(R+"b684b63cb0ba4646ac4380b436718fc4.json")))
sc_price = pd.DataFrame(json.load(open(R+"c8ae543682c84e9d9e8b0d6d10fb1eb8.json")))

# --- province volatility & variance contribution
piv = sc_prov.pivot_table(index="month", columns="province", values="profit", aggfunc="sum").fillna(0).sort_index()
tot = piv.sum(axis=1)
prov_cv = (piv.std()/piv.mean()*100).sort_values(ascending=False)
print("=== Province CV of monthly profit (SC) ===")
print(prov_cv.round(1).to_string())
vt = tot.var()
print("\n=== Province contribution to SC monthly profit variance ===")
print(pd.Series({c: piv[c].cov(tot)/vt*100 for c in piv.columns}).sort_values(ascending=False).round(1).to_string())
print("\nProvince share of annual profit:")
print((piv.sum()/piv.sum().sum()*100).sort_values(ascending=False).round(1).to_string())

# --- Feb drop decomposition by product
p2 = sc_prod.pivot_table(index="month", columns="product", values="profit", aggfunc="sum").fillna(0).sort_index()
feb_drop = (p2.loc["2023-02"] - p2.loc["2023-01"]).sort_values()
print("\n=== Product contribution to Jan->Feb profit drop (total %.0f) ===" % feb_drop.sum())
print(feb_drop.round(0).to_string())
mar_reb = (p2.loc["2023-03"] - p2.loc["2023-02"]).sort_values(ascending=False)
print("\n=== Product contribution to Feb->Mar rebound (total %.0f) ===" % mar_reb.sum())
print(mar_reb.round(0).to_string())

# volume vs value decomposition of profit MoM
sc["profit_mom_pct"] = sc["profit"].pct_change()*100
sc["orders_mom_pct"] = sc["orders"].pct_change()*100
sc["apo"] = sc["revenue"]/sc["orders"]
sc["apo_mom_pct"] = sc["apo"].pct_change()*100
print("\n=== Profit vs orders vs avg-order-value MoM% ===")
print(sc[["month","profit_mom_pct","orders_mom_pct","apo_mom_pct"]].round(1).to_string())
print("corr(profit_mom, orders_mom) =", sc[["profit_mom_pct","orders_mom_pct"]].corr().iloc[0,1].round(3))
print("corr(profit_mom, apo_mom)   =", sc[["profit_mom_pct","apo_mom_pct"]].corr().iloc[0,1].round(3))

# stability of ratios
print("\ndiscount rate range: %.2f-%.2f%%" % (sc_price["discount_rate_pct"].min(), sc_price["discount_rate_pct"].max()))
print("freight ratio range: %.2f-%.2f%%" % (sc_price["freight_ratio_pct"].min(), sc_price["freight_ratio_pct"].max()))
print("cost/revenue range: %.3f-%.3f" % ((sc["cost"]/sc["revenue"]).min(), (sc["cost"]/sc["revenue"]).max()))

# ============ CHARTS ============
months = sc["month"].str[2:].tolist()

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# A: indexed monthly profit by region (Jan=100)
ax = axes[0,0]
for reg, grp in region_m.groupby("region"):
    grp = grp.sort_values("month")
    idx = grp["profit"]/grp["profit"].iloc[0]*100
    ax.plot(grp["month"].str[2:], idx, marker="o", ms=3, label=reg,
            lw=2.5 if reg=="South China" else 1)
ax.set_title("A. Monthly profit index by region (Jan 2023 = 100)")
ax.legend(fontsize=7, ncol=2); ax.tick_params(axis='x', rotation=45, labelsize=7)

# B: SC profit vs orders
ax = axes[0,1]
ax2 = ax.twinx()
ax.bar(months, sc["profit"]/1000, color="steelblue", alpha=0.75, label="Profit (k)")
ax2.plot(months, sc["orders"], color="darkred", marker="o", label="Orders")
ax.set_title("B. South China: monthly profit vs order volume")
ax.set_ylabel("Profit (thousand)"); ax2.set_ylabel("Orders")
ax.tick_params(axis='x', rotation=45, labelsize=7)
ax2.legend(loc="lower right", fontsize=8)

# C: product monthly profit CV
ax = axes[1,0]
cv = (p2.std()/p2.mean()*100).sort_values()
ax.barh(cv.index, cv.values, color="teal")
ax.set_title("C. Monthly profit volatility by product, South China (CV %)")
for i,v in enumerate(cv.values): ax.text(v+0.3, i, f"{v:.1f}%", va="center", fontsize=8)

# D: MoM profit change decomposition: orders vs avg-order-value contribution
ax = axes[1,1]
d = sc.dropna(subset=["profit_mom_pct"])
# approx split of revenue growth into volume & value
vol_part = d["orders_mom_pct"]
val_part = d["apo_mom_pct"]
x = np.arange(len(d))
ax.bar(x-0.2, vol_part, 0.4, label="Order-volume effect (%)", color="orange")
ax.bar(x+0.2, val_part, 0.4, label="Avg-order-value effect (%)", color="gray")
ax.plot(x, d["profit_mom_pct"], color="navy", marker="o", label="Profit MoM (%)")
ax.set_xticks(x); ax.set_xticklabels(d["month"].str[2:], rotation=45, fontsize=7)
ax.axhline(0, color="k", lw=0.5)
ax.set_title("D. Drivers of South China MoM profit change")
ax.legend(fontsize=7)

plt.tight_layout()
plt.savefig("sc_profit_instability.png", dpi=130)
print("\nchart saved: sc_profit_instability.png")
