# dacomp-006 / pilot-01 查询与 Python 清单

Q 编号按该任务 SQL 尝试的开始时间排序，包含错误和元数据查询；P 编号独立。不同任务的 Q 编号不相关。

[展开 Python 工具后的全部 SQL 轨迹（含 list-db 和连接设置）](dacomp-006-pilot-01-SQL-TRAJECTORY.md)。本页 Q 编号仅对应 query-db 调用，不是全部数据库语句数。

GROUP BY 仅为语法清单，不等于跨查询下钻或复用机会。CTE 名称可能出现在表名清单中。

## 工具时间顺序

list-db → Q1 → Q2 → Q3 → Q4 → Q5 → Q6 → P1 → Q7 → Q8 → P2 → P3 → answer

SQL 结果文件在后续 Python 源码中的引用：Q3 → P1；Q4 → P1；Q6 → P1；Q3 → P2；Q4 → P2；Q6 → P2；Q7 → P2；Q8 → P2；Q6 → P3

## Q1 — 成功

结果行数：1；执行并取回：9.223 ms；元数据：False

```sql
SELECT MIN("Date") AS min_date, MAX("Date") AS max_date, COUNT(*) AS n_rows,
       COUNT(DISTINCT "Destination") AS n_dest
FROM sheet1
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/4c1c0a96fa9749ee860995a30d7c4bfb.json)

## Q2 — 成功

结果行数：277；执行并取回：12.038 ms；元数据：False

```sql
SELECT "Destination" AS dest, COUNT(*) AS n, ROUND(SUM("Profit"),2) AS total_profit
FROM sheet1
GROUP BY "Destination"
ORDER BY n DESC
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/46b9b15b9e5246ee9a9bf953a3939593.json)

## Q3 — 成功

结果行数：72；执行并取回：28.768 ms；元数据：False

```sql
SELECT
  CASE
    WHEN "Destination" LIKE 'South China%' THEN 'South China'
    WHEN "Destination" LIKE 'North China%' THEN 'North China'
    WHEN "Destination" LIKE 'East China%' THEN 'East China'
    WHEN "Destination" LIKE 'Northeast%' THEN 'Northeast'
    WHEN "Destination" LIKE 'Northwest%' THEN 'Northwest'
    WHEN "Destination" LIKE 'Southwest%' THEN 'Southwest'
    ELSE 'Other' END AS region,
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  ROUND(SUM("Profit"),2) AS profit,
  ROUND(SUM("Total Logistics Revenue"),2) AS revenue,
  ROUND(SUM("Total Logistics Cost"),2) AS cost
FROM sheet1
GROUP BY region, month
ORDER BY region, month
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/bbba0500d8ae439d9f4206db9bcd65b0.json)

## Q4 — 成功

结果行数：12；执行并取回：13.560 ms；元数据：False

```sql
SELECT
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  SUM("Sales Quantity") AS qty,
  ROUND(SUM("List Price Revenue"),2) AS list_rev,
  ROUND(SUM("Logistics Value-Added Service Revenue"),2) AS vas_rev,
  ROUND(SUM("Discount Amount"),2) AS discount,
  ROUND(SUM("Total Logistics Revenue"),2) AS revenue,
  ROUND(SUM("Freight Cost"),2) AS freight,
  ROUND(SUM("Warehousing Cost"),2) AS warehousing,
  ROUND(SUM("Other Operating Costs"),2) AS other_cost,
  ROUND(SUM("Total Logistics Cost"),2) AS cost,
  ROUND(SUM("Profit"),2) AS profit,
  ROUND(AVG("Profit Margin"),4) AS avg_margin
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY month
ORDER BY month
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/dba21aaa488a4a50844a2225fa3f465e.json)

## Q5 — 成功

结果行数：1；执行并取回：6.339 ms；元数据：False

```sql
SELECT
  COUNT(*) AS n,
  SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS neg_profit,
  SUM(CASE WHEN "Profit Margin" > 1 OR "Profit Margin" < 0 THEN 1 ELSE 0 END) AS bad_margin,
  ROUND(MIN("Profit"),2) AS min_profit,
  ROUND(MAX("Profit"),2) AS max_profit,
  ROUND(MIN("Profit Margin"),4) AS min_margin,
  ROUND(MAX("Profit Margin"),4) AS max_margin,
  ROUND(AVG("Profit"),2) AS avg_profit
FROM sheet1
WHERE "Destination" LIKE 'South China%'
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/2afde08295a04d8485ef68b1ad97974d.json)

## Q6 — 成功

结果行数：96；执行并取回：11.153 ms；元数据：False

```sql
SELECT "Consigned Product" AS product,
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  ROUND(SUM("Profit"),2) AS profit,
  SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS neg_orders,
  ROUND(SUM(CASE WHEN "Profit" < 0 THEN "Profit" ELSE 0 END),2) AS neg_profit_sum
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY product, month
ORDER BY product, month
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/91c3b0c7572b44eb898eca77acc81baf.json)

## Q7 — 成功

结果行数：72；执行并取回：14.896 ms；元数据：False

```sql
SELECT
  SUBSTR(SUBSTR("Destination", INSTR("Destination",'-')+1), 1,
         INSTR(SUBSTR("Destination", INSTR("Destination",'-')+1),'-')-1) AS province,
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  SUM("Sales Quantity") AS qty,
  ROUND(SUM("Total Logistics Revenue"),2) AS revenue,
  ROUND(SUM("Profit"),2) AS profit
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY province, month
ORDER BY province, month
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/b684b63cb0ba4646ac4380b436718fc4.json)

## Q8 — 成功

结果行数：12；执行并取回：11.260 ms；元数据：False

```sql
SELECT
  strftime('%Y-%m', "Date") AS month,
  ROUND(AVG("Logistics Unit Price"),2) AS avg_unit_price,
  ROUND(AVG("Sales Quantity"),1) AS avg_qty_per_order,
  ROUND(AVG("List Price Revenue"),2) AS avg_list_rev_per_order,
  ROUND(AVG("Discount Amount"),2) AS avg_discount,
  ROUND(AVG("Freight Cost"),2) AS avg_freight,
  ROUND(SUM("Discount Amount")/SUM("List Price Revenue")*100,3) AS discount_rate_pct,
  ROUND(SUM("Freight Cost")/SUM("Total Logistics Revenue")*100,3) AS freight_ratio_pct
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY month
ORDER BY month
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/c8ae543682c84e9d9e8b0d6d10fb1eb8.json)

## P1 — Python 成功

```python
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

```

[完整 stdout/stderr](../runs/natural/dacomp-006/pilot-01/results/4a6bd12134074f35943446e113e40ba3.json)

## P2 — Python 成功

```python
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

```

[完整 stdout/stderr](../runs/natural/dacomp-006/pilot-01/results/4e6ec46b04b642c8b21197a858667a99.json)

## P3 — Python 成功

```python
import json, pandas as pd
R = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/dacomp/runs/natural/dacomp-006/pilot-01/results/"
sc_prod = pd.DataFrame(json.load(open(R+"91c3b0c7572b44eb898eca77acc81baf.json")))
p2 = sc_prod.pivot_table(index="month", columns="product", values="profit", aggfunc="sum").fillna(0).sort_index()
share = (p2.sum()/p2.sum().sum()*100).sort_values(ascending=False)
print("Product share of SC annual profit (%):")
print(share.round(1).to_string())
print("\nOffice furniture monthly profit:")
print(p2["Office furniture"].round(0).to_string())
print("\nKitchen Appliances monthly profit:")
print(p2["Kitchen Appliances"].round(0).to_string())

```

[完整 stdout/stderr](../runs/natural/dacomp-006/pilot-01/results/4bec3965ed074143a74be0682a6badeb.json)
