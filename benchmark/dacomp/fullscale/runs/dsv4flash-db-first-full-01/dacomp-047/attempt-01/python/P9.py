import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

res = db.query("""
    SELECT pi."Item Name" AS name, strftime('%m', s."Sales Date") AS mo, 
           ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS avg_daily
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE pi."Item Name" IN ('Enoki Mushroom (box)','White Button Mushroom (box)','Bird''s-eye Chili (portion)',
      'Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)','Milk Bok Choy (portion)',
      'Wrinkled Pepper (portion)','Water Spinach','Sweet Potato Vine Tips')
      AND s."Sales Date" >= '2022-01-01'
    GROUP BY pi."Item Name", mo
    ORDER BY pi."Item Name", CAST(mo AS INT)
""")
cols = res['executions'][0]['columns']
rows = db.rows(res)
df = pd.DataFrame(rows, columns=cols)
df['avg_daily'] = df['avg_daily'].astype(float)

pivot = df.pivot_table(index='name', columns='mo', values='avg_daily', aggfunc='mean').fillna(0)
print("=== Monthly Avg Daily (2022+) for top 2023 candidates ===")
print(pivot.round(1))

# July seasonality index for these (July avg / overall avg)
pivot['overall'] = pivot.mean(axis=1)
pivot['july'] = pivot.get('07', 0)
pivot['july_seasonality'] = pivot['july'] / pivot['overall']
print("\n=== July Seasonality Index (2022+) ===")
print(pivot[['july','overall','july_seasonality']].round(3).sort_values('july_seasonality', ascending=False))

# Plot
plt.figure(figsize=(12, 7))
months = [str(i).zfill(2) for i in range(1,13)]
for name in pivot.index:
    if name in ['Water Spinach','Sweet Potato Vine Tips','Yunnan Leaf Lettuce (portion)',
                'Yunnan Romaine Lettuce (portion)','Bird’s-eye Chili (portion)','Wrinkled Pepper (portion)']:
        plt.plot(range(1,13), [pivot.loc[name, m] for m in months], marker='o', label=name)
plt.xlabel('Month')
plt.ylabel('Avg Daily Sales (kg)')
plt.title('2022-2023 Monthly Seasonality of Key Candidates')
plt.legend(bbox_to_anchor=(1.05,1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/key_candidates_seasonality.png', dpi=150)
plt.close()
print("Saved key_candidates_seasonality.png")