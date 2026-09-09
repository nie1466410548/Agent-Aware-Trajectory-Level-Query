
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Use the dataframe from the previous analysis - rebuild it
sql = """
WITH proc_items AS (
  SELECT s."Item Code", SUM(s."Sales volume (kg)") as vol_0630
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  GROUP BY s."Item Code"
),
summer_sales AS (
  SELECT s."Item Code",
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    strftime('%Y', s."Sales Date") as yr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
),
y2022 AS (
  SELECT "Item Code", COUNT(*) n22, AVG(profit) avgp22,
    SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*) pct22,
    SUM(vol*profit) tot22
  FROM summer_sales WHERE yr='2022' GROUP BY "Item Code"
)
SELECT pi."Item Code", p."Item Name", ROUND(pi.vol_0630,2) vol_0630,
  y.n22, ROUND(y.avgp22,3) avgp22, ROUND(y.pct22,1) pct22, ROUND(y.tot22,2) tot22
FROM proc_items pi
LEFT JOIN product_information p ON pi."Item Code" = p."Item Code"
LEFT JOIN y2022 y ON pi."Item Code" = y."Item Code"
ORDER BY COALESCE(y.avgp22, 999) ASC
"""
res = db.query(sql)
df = db.frame(res)
df = df[df['n22'].notna()].copy()  # keep items with 2022 summer data
df['label'] = df['Item Name'] + ' (' + df['Item Code'].astype(str) + ')'
df = df.sort_values('avgp22', ascending=True)

fig, ax = plt.subplots(figsize=(12, 9))
colors = ['#d62728' if v < 0.1 else '#1f77b4' for v in df['avgp22']]
bars = ax.barh(df['label'], df['avgp22'], color=colors, edgecolor='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=1.2)
ax.set_xlabel('Avg profit per kg (yuan) - 2022 summer (Unit price - Wholesale/(1-loss rate))')
ax.set_title('Profitability of items procured on 2023-07-01 (based on 2023-06-30 sales) \nusing previous summer (2022, Jun-Aug) sales data')
ax.grid(axis='x', alpha=0.3)
for i, (idx, row) in enumerate(df.iterrows()):
    ax.text(row['avgp22'] + 0.05, i, f"{row['avgp22']:.2f} | loss {row['pct22']:.0f}%", va='center', fontsize=8)
plt.tight_layout()
plt.savefig('work/summer_profitability_2022.png', dpi=130)
print("saved figure")

# Also summarize the two clear candidates
print(df.head(6)[['Item Code','Item Name','vol_0630','n22','avgp22','pct22','tot22']].to_string())
