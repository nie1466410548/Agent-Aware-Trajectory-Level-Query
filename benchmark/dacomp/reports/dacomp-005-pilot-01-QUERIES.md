# dacomp-005 / pilot-01 查询与 Python 清单

Q 编号按该任务 SQL 尝试的开始时间排序，包含错误和元数据查询；P 编号独立。不同任务的 Q 编号不相关。

GROUP BY 仅为语法清单，不等于跨查询下钻或复用机会。CTE 名称可能出现在表名清单中。

## 工具时间顺序

list-db → Q1 → Q2 → Q3 → Q4 → Q5 → Q6 → Q7 → Q8 → Q9 → Q10 → Q11 → P1 → answer

SQL 结果文件在后续 Python 源码中的引用：Q11 → P1

## Q1 — 失败

结果行数：—；执行并取回：0.000 ms；元数据：False

```sql
SELECT COUNT(*) AS n_orders,
AVG("Profit Margin") AS avg_margin,
AVG("Profit Margin")*0.5 AS low_margin_threshold,
SUM(CASE WHEN "Profit Margin" < AVG("Profit Margin")*0.5 THEN 1 ELSE 0 END) AS dummy_check,
MIN("Profit Margin") AS min_margin, MAX("Profit Margin") AS max_margin,
MIN("Date") AS min_date, MAX("Date") AS max_date
FROM sheet1

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/4a15592a1b6449f4b4ffd3d258a7f7b7.json)

OperationalError: misuse of aggregate function AVG()

## Q2 — 成功

结果行数：1；执行并取回：6.552 ms；元数据：False

```sql
SELECT COUNT(*) AS n_orders,
AVG("Profit Margin") AS avg_margin,
AVG("Profit Margin")*0.5 AS low_margin_threshold,
MIN("Profit Margin") AS min_margin, MAX("Profit Margin") AS max_margin,
MIN("Date") AS min_date, MAX("Date") AS max_date
FROM sheet1

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/05de7e1131794d5bb7e853aabb23e5b1.json)

## Q3 — 成功

结果行数：10；执行并取回：0.214 ms；元数据：False

```sql
SELECT "Total Logistics Revenue" AS rev, "Total Logistics Cost" AS cost, "Profit" AS profit,
"Profit Margin" AS margin,
ROUND("Profit"/"Total Logistics Revenue",4) AS pm_rev,
ROUND("Profit"/"Total Logistics Cost",4) AS pm_cost
FROM sheet1 LIMIT 10

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/468a805fa65b40819da5b12143420e53.json)

## Q4 — 成功

结果行数：2；执行并取回：29.816 ms；元数据：False

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS grp,
COUNT(*) AS n,
AVG("Sales Quantity") AS avg_qty,
AVG("Total Logistics Revenue") AS avg_rev,
SUM("Total Logistics Revenue") AS sum_rev,
SUM("Profit") AS sum_profit,
AVG("Profit") AS avg_profit,
AVG("List Price Revenue") AS avg_list,
AVG("Logistics Value-Added Service Revenue") AS avg_vas,
AVG("Discount Amount") AS avg_disc,
AVG("Discount Amount"/"List Price Revenue") AS avg_disc_rate,
AVG("Freight Cost") AS avg_freight,
AVG("Warehousing Cost") AS avg_wh,
AVG("Other Operating Costs") AS avg_other,
AVG("Total Logistics Cost") AS avg_cost,
AVG("Total Logistics Cost"/"Sales Quantity") AS cost_per_unit,
AVG("Customer Age") AS avg_age,
SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS n_loss
FROM sheet1 GROUP BY grp

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/a3f12d18c9174fdab455f28afd5d50e8.json)

## Q5 — 成功

结果行数：99；执行并取回：9.828 ms；元数据：False

```sql
SELECT "Sales Quantity" AS qty, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low
FROM sheet1 GROUP BY qty ORDER BY qty

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/f69754f57e9a418fae065861e3b57f52.json)

## Q6 — 成功

结果行数：277；执行并取回：17.483 ms；元数据：False

```sql
SELECT "Destination" AS dest, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty,
ROUND(AVG("Freight Cost"),1) AS avg_freight,
ROUND(AVG("Total Logistics Cost"),1) AS avg_cost
FROM sheet1 GROUP BY dest ORDER BY low_pct DESC

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/ff1d52c467044dada27adbc895c214f7.json)

## Q7 — 成功

结果行数：8；执行并取回：14.753 ms；元数据：False

```sql
SELECT "Consigned Product" AS prod, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty,
ROUND(AVG("Discount Amount"/"List Price Revenue")*100,2) AS avg_disc_pct,
ROUND(AVG("Profit Margin"),3) AS avg_margin
FROM sheet1 GROUP BY prod ORDER BY low_pct DESC

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/793509e81c254204b2164410103c016f.json)

## Q8 — 成功

结果行数：6；执行并取回：17.975 ms；元数据：False

```sql
SELECT SUBSTR("Destination",1,INSTR("Destination",'-')-1) AS region, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty,
ROUND(AVG("Freight Cost"),1) AS avg_freight,
ROUND(AVG("Total Logistics Cost"),1) AS avg_cost,
ROUND(AVG("Profit Margin"),3) AS avg_margin
FROM sheet1 GROUP BY region ORDER BY low_pct DESC

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/1704b01a214d47888089d2a12790dcd6.json)

## Q9 — 成功

结果行数：10；执行并取回：17.655 ms；元数据：False

```sql
SELECT "Age Range" AS ar, "Customer Gender" AS g, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty,
ROUND(AVG("Profit Margin"),3) AS avg_margin
FROM sheet1 GROUP BY ar, g ORDER BY ar, g

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/fee046c8edd84ffaba47ab6efd4b643c.json)

## Q10 — 成功

结果行数：12；执行并取回：19.081 ms；元数据：False

```sql
SELECT STRFTIME('%Y-%m',"Date") AS ym, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Profit Margin"),3) AS avg_margin,
ROUND(AVG("Discount Amount"/"List Price Revenue")*100,2) AS avg_disc_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty
FROM sheet1 GROUP BY ym ORDER BY ym

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/165d9e972a674fa189f5a4908c26ec47.json)

## Q11 — 成功

结果行数：18250；执行并取回：68.269 ms；元数据：False

```sql
SELECT "Date", "Destination", "Customer Gender", "Customer Age", "Age Range",
"Consigned Product", "Sales Quantity", "Logistics Unit Price", "List Price Revenue",
"Logistics Value-Added Service Revenue", "Discount Amount", "Total Logistics Revenue",
"Freight Cost", "Warehousing Cost", "Other Operating Costs", "Total Logistics Cost",
"Profit", "Profit Margin" FROM sheet1

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/6535ec41c6fb4e4ab3a53106bbf9a323.json)

## P1 — Python 成功

```python
import json, numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/dacomp/runs/natural/dacomp-005/pilot-01/results/6535ec41c6fb4e4ab3a53106bbf9a323.json') as f:
    df = pd.DataFrame(json.load(f))

thr = df['Profit Margin'].mean() * 0.5
df['low'] = df['Profit Margin'] < thr
df['disc_rate'] = df['Discount Amount'] / df['List Price Revenue']
df['cpu'] = df['Total Logistics Cost'] / df['Sales Quantity']
df['vas_share'] = df['Logistics Value-Added Service Revenue'] / df['Total Logistics Revenue']
df['region'] = df['Destination'].str.split('-').str[0]

print("threshold:", round(thr,6), "| n low:", df['low'].sum(), f"({df['low'].mean()*100:.2f}%)")
print("low-margin profit sum:", round(df.loc[df['low'],'Profit'].sum(),2),
      "| loss orders:", (df.loc[df['low'],'Profit']<0).sum(),
      "| loss profit sum:", round(df.loc[df['low'] & (df['Profit']<0),'Profit'].sum(),2))
print("share of total revenue from low:", round(df.loc[df['low'],'Total Logistics Revenue'].sum()/df['Total Logistics Revenue'].sum()*100,2),"%")

# quantity bands
bands = [0,5,10,15,20,25,30,35,50,100]
df['qb'] = pd.cut(df['Sales Quantity'], bands)
t = df.groupby('qb', observed=True).agg(n=('low','size'), low_rate=('low','mean'),
    avg_margin=('Profit Margin','mean'), avg_cost=('Total Logistics Cost','mean'),
    avg_rev=('Total Logistics Revenue','mean'), avg_disc=('disc_rate','mean'),
    avg_cpu=('cpu','mean'))
t['low_rate']=(t['low_rate']*100).round(2); t[['avg_margin','avg_disc','avg_cpu']] = t[['avg_margin','avg_disc','avg_cpu']].round(3)
t[['avg_cost','avg_rev']] = t[['avg_cost','avg_rev']].round(1)
print("\nBy quantity band:\n", t)

print("\nlow orders with qty<=10:", ((df['low'])&(df['Sales Quantity']<=10)).sum(),
      f"({(df['low']&(df['Sales Quantity']<=10)).sum()/df['low'].sum()*100:.1f}% of low)")
print("low orders with qty<=32:", ((df['low'])&(df['Sales Quantity']<=32)).sum(),
      f"({(df['low']&(df['Sales Quantity']<=32)).sum()/df['low'].sum()*100:.1f}% of low)")
print("share of all orders qty<=32:", round((df['Sales Quantity']<=32).mean()*100,2),"%")
print("low rate among qty<=32:", round(df.loc[df['Sales Quantity']<=32,'low'].mean()*100,2),"%")

# discount bands
db = pd.cut(df['disc_rate'], [-0.001,0,0.02,0.05,0.10,0.20,0.50,1.0])
td = df.groupby(db, observed=True).agg(n=('low','size'), low_rate=('low','mean'),
      avg_margin=('Profit Margin','mean'), avg_qty=('Sales Quantity','mean'))
td['low_rate']=(td['low_rate']*100).round(2)
print("\nBy discount-rate band:\n", td.round(3))
print("\nlow orders disc_rate>5%:", round((df.loc[df['low'],'disc_rate']>0.05).mean()*100,1),"%",
      "| normal:", round((df.loc[~df['low'],'disc_rate']>0.05).mean()*100,1),"%")
print("median disc rate low:", round(df.loc[df['low'],'disc_rate'].median()*100,2),
      "| normal:", round(df.loc[~df['low'],'disc_rate'].median()*100,2))

# correlations with low flag / margin (numeric drivers)
num = ['Sales Quantity','Logistics Unit Price','List Price Revenue','Logistics Value-Added Service Revenue',
       'Discount Amount','Total Logistics Revenue','Freight Cost','Warehousing Cost','Other Operating Costs',
       'Total Logistics Cost','Customer Age','disc_rate','cpu','vas_share']
print("\nPoint-biserial corr with low flag:\n", df[num].corrwith(df['low'].astype(int)).sort_values(ascending=False).round(3))
print("\nSpearman corr of Sales Quantity with Total Logistics Cost:", round(df['Sales Quantity'].corr(df['Total Logistics Cost'],method='spearman'),4))

# cost structure shares
for grp,sub in [('low',df[df['low']]),('normal',df[~df['low']])]:
    tot = sub[['Freight Cost','Warehousing Cost','Other Operating Costs']].sum()
    print(grp, "cost mix %:", (tot/tot.sum()*100).round(1).to_dict())

# cost per unit by quantity band for ALL orders
print("\ncost per unit by qty band:\n", df.groupby('qb', observed=True)['cpu'].mean().round(2))

# breakeven / remediation simulation for low-margin orders
low = df[df['low']].copy()
# required revenue to reach avg-margin and threshold-margin given actual cost
low['req_rev_avg'] = low['Total Logistics Cost']/(1-df['Profit Margin'].mean())
low['req_rev_thr'] = low['Total Logistics Cost']/(1-thr)
print("\nlow orders: mean actual rev", round(low['Total Logistics Revenue'].mean(),1),
      "| mean rev needed for avg margin:", round(low['req_rev_avg'].mean(),1),
      "| mean rev needed for thr margin:", round(low['req_rev_thr'].mean(),1))
# quantity needed (revenue scales ~ linearly with qty at same unit economics)
low['rev_per_unit'] = low['Total Logistics Revenue']/low['Sales Quantity']
low['qty_needed_avg'] = np.ceil(low['req_rev_avg']/low['rev_per_unit'])
low['qty_needed_thr'] = np.ceil(low['req_rev_thr']/low['rev_per_unit'])
print("median qty now:", low['Sales Quantity'].median(), "| median qty needed (avg margin):", low['qty_needed_avg'].median(),
      "| median qty needed (thr margin):", low['qty_needed_thr'].median())
# cost reduction simulation: cut cost 20% on low orders
sim = low['Total Logistics Revenue'] - low['Total Logistics Cost']*0.8
print("if cost cut 20%: low orders turning non-negative profit:", round((sim>0).mean()*100,1),"%",
      "| total low-segment profit now:", round(low['Profit'].sum(),1), "->", round(sim.sum(),1))
# eliminate discount on low orders
sim2 = low['Profit'] + low['Discount Amount']
print("if discounts removed on low orders: total low-segment profit:", round(low['Profit'].sum(),1), "->", round(sim2.sum(),1),
      "| still loss:", (sim2<0).sum())
# minimum order qty=20 simulation: merge would raise rev per order; approximate: scale qty to 20
sim3 = low['rev_per_unit']*20 - low['Total Logistics Cost']
print("if all low orders had qty=20: total profit:", round(sim3.sum(),1), "| share positive:", round((sim3>0).mean()*100,1),"%")

# VAS revenue
print("\nVAS share of revenue low vs normal:", round(low['vas_share'].mean()*100,2), round(df.loc[~df['low'],'vas_share'].mean()*100,2))
print("VAS per order low vs normal:", round(low['Logistics Value-Added Service Revenue'].mean(),2), round(df.loc[~df['low'],'Logistics Value-Added Service Revenue'].mean(),2))

# monthly low rate for chart
df['ym'] = pd.to_datetime(df['Date']).dt.to_period('M').astype(str)
mo = df.groupby('ym')['low'].mean()*100

# ---- charts ----
fig, axes = plt.subplots(2,2, figsize=(13,10))
ax=axes[0,0]
qr = df.groupby('Sales Quantity')['low'].mean()*100
ax.plot(qr.index, qr.values, marker='.', ms=3)
ax.set_xlabel('Sales Quantity'); ax.set_ylabel('% low-margin orders')
ax.set_title('Low-margin rate vs Sales Quantity')
ax.axvline(32, color='r', ls='--', lw=1, label='qty=32 cutoff'); ax.legend()

ax=axes[0,1]
ax.hist(df.loc[~df['low'],'disc_rate']*100, bins=50, alpha=0.6, label='normal', density=True)
ax.hist(df.loc[df['low'],'disc_rate']*100, bins=50, alpha=0.6, label='low-margin', density=True)
ax.set_xlabel('Discount rate (% of List Price Revenue)'); ax.set_ylabel('density')
ax.set_title('Discount-rate distribution'); ax.legend()

ax=axes[1,0]
sub = df.sample(4000, random_state=1)
ax.scatter(sub.loc[~sub['low'],'Total Logistics Revenue'], sub.loc[~sub['low'],'Total Logistics Cost'], s=4, alpha=0.4, label='normal')
ax.scatter(sub.loc[sub['low'],'Total Logistics Revenue'], sub.loc[sub['low'],'Total Logistics Cost'], s=6, alpha=0.7, c='r', label='low-margin')
xs = np.linspace(0, df['Total Logistics Revenue'].max(), 50)
ax.plot(xs, xs*(1-thr), 'g--', lw=1, label='margin=threshold')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('Total Logistics Revenue'); ax.set_ylabel('Total Logistics Cost')
ax.set_title('Revenue vs Cost (log-log)'); ax.legend()

ax=axes[1,1]
mo.plot(ax=ax, marker='o')
ax.set_ylabel('% low-margin orders'); ax.set_title('Monthly low-margin rate (2023)')
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
plt.tight_layout(); plt.savefig('low_margin_overview.png', dpi=110)
print("\nsaved low_margin_overview.png")

# cost mix comparison chart
fig, ax = plt.subplots(figsize=(7,4.5))
labels=['Freight Cost','Warehousing Cost','Other Operating Costs']
lm = [low[c].mean() for c in labels]; nm = [df.loc[~df['low'],c].mean() for c in labels]
x=np.arange(3); w=0.35
ax.bar(x-w/2, nm, w, label='normal'); ax.bar(x+w/2, lm, w, label='low-margin')
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylabel('avg cost per order')
ax.set_title('Average cost components per order'); ax.legend()
plt.tight_layout(); plt.savefig('cost_components.png', dpi=110)
print("saved cost_components.png")

```

[完整 stdout/stderr](../runs/natural/dacomp-005/pilot-01/results/4e8ed73a8f4b42a4a95a559da875b8e1.json)
