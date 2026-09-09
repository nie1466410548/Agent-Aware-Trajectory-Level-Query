import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Pull monthly avg daily for 2023 candidates
res = db.query("""
    SELECT pi."Item Name" AS name, strftime('%Y-%m', s."Sales Date") AS ym,
           SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date") AS avg_daily
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Sales Date" >= '2022-10-01'
    GROUP BY pi."Item Name", ym
    HAVING SUM(s."Sales volume (kg)") > 50
    ORDER BY pi."Item Name", ym
""")
cols = res['executions'][0]['columns']
rows = db.rows(res)
trend = pd.DataFrame(rows, columns=cols)
trend['avg_daily'] = trend['avg_daily'].astype(float)

# Pivot: rows = item, cols = month
pivot = trend.pivot_table(index='name', columns='ym', values='avg_daily', aggfunc='mean').fillna(0)

# Focus on 2023 months
months_2023 = [c for c in pivot.columns if c.startswith('2023')]
months_late22 = [c for c in pivot.columns if c.startswith('2022')]
pivot23 = pivot[months_2023]

# Compute growth metrics
pivot23['h1_2023_avg'] = pivot23[['2023-01','2023-02','2023-03','2023-04','2023-05','2023-06']].mean(axis=1)
pivot23['jun23'] = pivot23.get('2023-06', 0)
pivot23['may23'] = pivot23.get('2023-05', 0)
pivot23['recent_trend'] = pivot23['jun23'] - pivot23['may23']

# Sort by most recent month
top_recent = pivot23.sort_values('jun23', ascending=False)
print("=== Top 30 Items by June 2023 Daily Avg Sales ===")
print(top_recent.head(30)[['2023-04','2023-05','2023-06','h1_2023_avg','recent_trend']].round(2).to_string())

# Items with rising trend into June
rising = pivot23[pivot23['recent_trend'] > 0].sort_values('recent_trend', ascending=False)
print("\n=== Items with Rising June 2023 (positive month-over-month change) ===")
print(rising.head(20)[['2023-05','2023-06','recent_trend']].round(2).to_string())

# Save for reference
pivot.to_csv('/work/2023_trend.csv')