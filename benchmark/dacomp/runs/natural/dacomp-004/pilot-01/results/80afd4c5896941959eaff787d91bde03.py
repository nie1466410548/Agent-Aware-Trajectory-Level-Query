import json
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/dacomp/runs/natural/dacomp-004/pilot-01/results/"
monthly = pd.DataFrame(json.load(open(BASE + "2fc1c0146100445081c7fdd47f1937d0.json")))  # per product-month totals
repeat = pd.DataFrame(json.load(open(BASE + "d0df8843606e406f8156470eed9c0525.json")))  # repeat customers
single = pd.DataFrame(json.load(open(BASE + "98002727db954c149289a902ee91f9eb.json")))
totals = pd.DataFrame(json.load(open(BASE + "4769620749024d0f83cc505eff3c8911.json")))

# 1. Top product per month by aggregated sales
top = monthly.loc[monthly.groupby("month")["total_sales"].idxmax()].sort_values("month")
print("=== TOP PRODUCT PER MONTH (by total monthly Sales Amount) ===")
print(top.to_string(index=False))

# share of month total
top = top.merge(totals[["month", "total_sales"]].rename(columns={"total_sales": "month_total"}), on="month")
top["share_pct"] = (100 * top["total_sales"] / top["month_total"]).round(2)
print(top[["month", "product_code", "total_sales", "month_total", "share_pct"]].to_string(index=False))

# runner-up per month for context
r = monthly.sort_values(["month", "total_sales"], ascending=[True, False])
second = r.groupby("month").nth(1).reset_index()
print("=== RUNNERS-UP ===")
print(second[["month", "product_code", "total_sales"]].to_string(index=False))

# 2. Repurchase rate per product-month = repeat customers / distinct customers
rep = monthly.merge(repeat, on=["product_code", "month"], how="left")
rep["repeat_customers"] = rep["repeat_customers"].fillna(0)
rep["repurchase_rate"] = rep["repeat_customers"] / rep["n_customers"]

top_codes = top["product_code"].tolist()
print("Top product codes:", top_codes)

focus = rep[rep["product_code"].isin(top_codes)].sort_values(["product_code", "month"])
print("=== PERFORMANCE OF MONTHLY TOP PRODUCTS ACROSS MONTHS ===")
cols = ["product_code", "minor_category", "month", "txn_count", "n_customers", "repeat_customers", "total_sales", "repurchase_rate"]
focus_out = focus[cols].copy()
focus_out["repurchase_rate"] = (100 * focus_out["repurchase_rate"]).round(1)
print(focus_out.to_string(index=False))

# full-period totals for focus products
fp = rep[rep["product_code"].isin(top_codes)].groupby("product_code").agg(
    months_present=("month", "nunique"),
    total_sales_4m=("total_sales", "sum"),
    total_customers=("n_customers", "sum"),
    total_repeat=("repeat_customers", "sum"),
    total_txn=("txn_count", "sum"))
fp["overall_repurchase_rate"] = fp["total_repeat"] / fp["total_customers"]
print("=== 4-MONTH SUMMARY OF TOP PRODUCTS ===")
print(fp.round(3).to_string())

# 3. Relationship repurchase rate vs sales amount (all product-months, min 5 customers to reduce noise)
d = rep[rep["n_customers"] >= 5].copy()
print(f"\nProduct-months with >=5 customers: {len(d)}")
r_pear, p_pear = stats.pearsonr(d["repurchase_rate"], d["total_sales"])
r_spear, p_spear = stats.spearmanr(d["repurchase_rate"], d["total_sales"])
print(f"ALL PRODUCTS: Pearson r={r_pear:.4f} (p={p_pear:.4g}), Spearman rho={r_spear:.4f} (p={p_spear:.4g})")

# log scale
r_log, p_log = stats.pearsonr(d["repurchase_rate"], np.log10(d["total_sales"]))
print(f"vs log10(sales): Pearson r={r_log:.4f} (p={p_log:.4g})")

# also n_repeaters absolute vs sales
r2, p2 = stats.pearsonr(d["repeat_customers"], d["total_sales"])
print(f"repeat_customers (count) vs sales: Pearson r={r2:.4f} (p={p2:.4g})")

# focus products only across months
df = rep[rep["product_code"].isin(top_codes)]
if len(df) >= 4:
    rf, pf = stats.pearsonr(df["repurchase_rate"], df["total_sales"])
    rsf, psf = stats.spearmanr(df["repurchase_rate"], df["total_sales"])
    print(f"TOP-PRODUCTS ONLY (n={len(df)}): Pearson r={rf:.4f} (p={pf:.4g}), Spearman rho={rsf:.4f} (p={psf:.4g})")

# correlation of customer count vs sales (context)
r3, p3 = stats.pearsonr(d["n_customers"], d["total_sales"])
print(f"n_customers vs sales: Pearson r={r3:.4f} (p={p3:.4g})")

# ---- Charts ----
# Chart 1: top product sales by month + focus products monthly trends
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax = axes[0]
labels = [f"{m}\n{c}" for m, c in zip(top["month"], top["product_code"])]
ax.bar(labels, top["total_sales"], color="#4C72B0")
ax.set_title("Top-selling product per month\n(by aggregated monthly Sales Amount)")
ax.set_ylabel("Monthly Sales Amount")
for i, v in enumerate(top["total_sales"]):
    ax.text(i, v, f"{v:,.0f}", ha="center", va="bottom", fontsize=9)

ax = axes[1]
for code in top_codes:
    sub = rep[rep["product_code"] == code].sort_values("month")
    ax.plot(sub["month"].astype(str), sub["total_sales"], marker="o", label=code)
ax.set_title("Monthly Sales trend of monthly top products")
ax.set_ylabel("Monthly Sales Amount")
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig("top_products_by_month.png", dpi=110)
plt.close()

# Chart 2: repurchase rate vs sales scatter
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax = axes[0]
ax.scatter(d["repurchase_rate"], d["total_sales"], alpha=0.25, s=12, color="#4C72B0", label="All product-months (>=5 customers)")
hl = rep[rep["product_code"].isin(top_codes)]
ax.scatter(hl["repurchase_rate"], hl["total_sales"], color="#DD8452", s=60, edgecolor="k", zorder=5, label="Monthly top products")
for _, row in hl.iterrows():
    ax.annotate(str(row["month"])[4:], (row["repurchase_rate"], row["total_sales"]), fontsize=8, xytext=(4, 4), textcoords="offset points")
ax.set_xlabel("Repurchase rate (share of customers buying >=2x in month)")
ax.set_ylabel("Monthly Sales Amount")
ax.set_title(f"Repurchase rate vs Sales (Spearman rho={r_spear:.3f})")
ax.legend(fontsize=8)

ax = axes[1]
ax.scatter(d["repurchase_rate"], d["total_sales"], alpha=0.25, s=12, color="#4C72B0")
ax.scatter(hl["repurchase_rate"], hl["total_sales"], color="#DD8452", s=60, edgecolor="k", zorder=5)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("Repurchase rate (log)")
ax.set_ylabel("Monthly Sales Amount (log)")
ax.set_title("Log-log view")
plt.tight_layout()
plt.savefig("repurchase_vs_sales.png", dpi=110)
plt.close()

# Chart 3: focus products repurchase rate trend
fig, ax = plt.subplots(figsize=(8, 5))
for code in top_codes:
    sub = rep[rep["product_code"] == code].sort_values("month")
    ax.plot(sub["month"].astype(str), sub["repurchase_rate"] * 100, marker="s", label=code)
ax.set_title("Monthly repurchase rate of monthly top products")
ax.set_ylabel("Repurchase rate (%)")
ax.legend(fontsize=8)
plt.tight_layout()
plt.savefig("repurchase_trend_top_products.png", dpi=110)
plt.close()

print("Charts saved.")
