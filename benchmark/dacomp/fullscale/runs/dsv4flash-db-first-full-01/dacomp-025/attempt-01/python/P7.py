import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Figure: 2022 summer monthly avg selling price vs effective cost for the two candidate items
sql = """
WITH summer_analysis AS (
  SELECT s."Item Code",
    strftime('%m', s."Sales Date") as mo,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Item Code" IN (102900005118824, 102900011032732)
    AND s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code", mo, COUNT(*) n, AVG(up) avg_up, AVG(wp/(1.0-lr/100.0)) avg_cost
FROM summer_analysis GROUP BY "Item Code", mo
"""
res = db.query(sql)
df = db.frame(res)
names = {102900005118824:'Gao Gua (1)', 102900011032732:'Gao Gua (2)'}

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
for ax, (code, name) in zip(axes, names.items()):
    sub = df[df['Item Code']==code].sort_values('mo')
    x = np.arange(len(sub))
    w = 0.35
    ax.bar(x-w/2, sub['avg_up'], w, label='Avg selling price', color='#2e8b57')
    ax.bar(x+w/2, sub['avg_cost'], w, label='Effective cost (wholesale/(1-loss))', color='#d62728')
    ax.set_xticks(x)
    ax.set_xticklabels([f"2022-{int(m):02d}" for m in sub['mo']])
    ax.set_title(f"{name} ({code})")
    ax.legend(fontsize=8)
    ax.set_ylabel('yuan/kg')
    ax.grid(alpha=0.3)
plt.suptitle('2022 summer: selling price vs effective cost (procurement would be loss-making where red > green)')
plt.tight_layout()
plt.savefig('work/gaogua_price_vs_cost.png', dpi=130)
print('saved second figure')

# Final summary numbers for the report
print("--- 2023-06-30 direct evidence ---")
sql3 = """
SELECT s."Item Code", p."Item Name",
  COUNT(*) n_sales,
  ROUND(SUM(s."Sales volume (kg)"),2) vol,
  ROUND(AVG(s."Unit price (yuan/kg)"),2) avg_up,
  ROUND(AVG(pp."Wholesale price (yuan/kg)"),2) avg_wp,
  ROUND(AVG(pp."Wholesale price (yuan/kg)")/(1.0-pl."Loss Rate (%)"/100.0),2) avg_cost,
  ROUND(SUM(CASE WHEN s."Unit price (yuan/kg)" < pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) THEN 1 ELSE 0 END)*100.0/COUNT(*),1) pct_loss_sales
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  AND s."Item Code" IN (102900005118824, 102900011032732)
  AND pp."Wholesale price (yuan/kg)" IS NOT NULL
GROUP BY s."Item Code"
"""
res3 = db.query(sql3)
df3 = db.frame(res3)
print(df3.to_string())
