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
