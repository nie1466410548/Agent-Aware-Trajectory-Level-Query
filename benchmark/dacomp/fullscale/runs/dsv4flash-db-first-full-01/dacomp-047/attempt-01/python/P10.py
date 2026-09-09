import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Create a combined multi-panel figure
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Category correlation heatmap
cat_res = db.query("SELECT strftime('%Y-%m-%d', \"Sales Date\") AS d, pi.\"Category Name\" AS cat, SUM(\"Sales volume (kg)\") AS vol FROM sales_records s JOIN product_information pi ON s.\"Item Code\"=pi.\"Item Code\" GROUP BY d, cat")
cat_cols = cat_res['executions'][0]['columns']
cat_rows = db.rows(cat_res)
cat_df = pd.DataFrame(cat_rows, columns=cat_cols)
cat_pivot = cat_df.pivot_table(index='d', columns='cat', values='vol', aggfunc='sum').fillna(0)
sns.heatmap(cat_pivot.corr(), annot=True, cmap='RdBu_r', center=0, vmin=-0.3, vmax=1, 
            fmt='.2f', ax=axes[0,0])
axes[0,0].set_title('Category Daily Sales Correlation', fontsize=12)

# 2. July seasonality index for key items
items = ['Yunnan Leaf Lettuce\n(portion)', 'Water Spinach', 'Sweet Potato\nVine Tips', 
         'Broccoli', 'Yunnan Romaine\nLettuce (portion)', 'Purple\nEggplant (2)',
         'Milk Bok Choy\n(portion)', 'Yellow Chinese\nCabbage (2)', 'Shanghai\nBok Choy',
         'White Button\nMushroom (box)', 'Spiral\nchili pepper', 'Bird\'s-eye\nChili (portion)']
seas = [1.05, 2.45, 3.27, 1.22, 1.23, 1.09, 1.22, 1.77, 1.20, 1.04, 1.17, 0.57]
colors = ['#2ecc71' if s > 1.0 else '#e74c3c' for s in seas]
bars = axes[0,1].barh(items, seas, color=colors)
axes[0,1].axvline(x=1.0, color='gray', linestyle='--', alpha=0.7)
axes[0,1].set_xlabel('July Seasonality Index (>1.0 = July peak)')
axes[0,1].set_title('July Seasonality of Key Candidate Items', fontsize=12)

# 3. Top 2023 items with June trend
trend_data = {'Yunnan Leaf Lettuce (portion)': 36.83,
              'Bird\'s-eye Chili (portion)': 22.87,
              'Yunnan Romaine Lettuce (portion)': 22.67,
              'Water Spinach': 14.45,
              'Broccoli': 14.35,
              'White Button Mushroom (box)': 13.37,
              'Milk Bok Choy (portion)': 12.06,
              'Purple Eggplant (2)': 15.73,
              'Sweet Potato Vine Tips': 6.34}
items2 = list(trend_data.keys())
vals = list(trend_data.values())
bars2 = axes[1,0].barh(items2, vals, color='#3498db')
axes[1,0].set_xlabel('Avg Daily Sales (kg) - June 2023')
axes[1,0].set_title('Recent Sales Level (June 2023)', fontsize=12)

# 4. Recommended combinations summary
axes[1,1].axis('off')
text = """RECOMMENDED THREE COMBINATIONS FOR JULY 2023

Combination 1: Summer Leafy Greens
-----------------------
• Yunnan Leaf Lettuce (portion)
• Water Spinach
• Sweet Potato Vine Tips
→ July seasonality: 1.05, 2.45, 3.27
→ Rising trend, complementary pairs

Combination 2: Cross-Category Staples
-----------------------
• Broccoli
• Yunnan Romaine Lettuce (portion)
• Purple Eggplant (2)
→ July seasonality: 1.22, 1.23, 1.09
→ Category diversity, high volume

Combination 3: Chinese Greens & Chili
-----------------------
• Milk Bok Choy (portion)
• Yellow Chinese Cabbage (2)
• Bird's-eye Chili (portion)
→ July seasonality: 1.22, 1.77, 0.57
→ Traditional cooking staples"""

axes[1,1].text(0.05, 0.95, text, transform=axes[1,1].transAxes, fontsize=10,
               verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('/work/final_recommendation.png', dpi=150)
plt.close()
print("Saved final_recommendation.png")