import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Check what's available
print("CWD:", os.getcwd())
print("Files in /results:", os.listdir('/results')[:20] if os.path.isdir('/results') else 'no /results dir')

# Try reading the file
df = pd.read_json('/results/S10.rows.jsonl', lines=True)
df.columns = ['Major_Category', 'Sales_Month', 'Monthly_Amount', 'Monthly_Qty', 'Trans_Count']
df['Month'] = df['Sales_Month'].astype(str).str[4:6].astype(int)
df['Month_Label'] = df['Month'].map({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr'})

# ========== FIGURE 1: Top 8 categories line chart ==========
top8 = df.groupby('Major_Category')['Monthly_Amount'].sum().sort_values(ascending=False).head(8).index.tolist()
df_top8 = df[df['Major_Category'].isin(top8)].copy()

plt.figure(figsize=(14, 7))
sns.set_style("whitegrid")
colors = sns.color_palette("husl", 8)
for i, cat in enumerate(top8):
    cat_df = df_top8[df_top8['Major_Category'] == cat].sort_values('Sales_Month')
    plt.plot(cat_df['Month_Label'], cat_df['Monthly_Amount'], marker='o', linewidth=2.5, 
             label=cat, color=colors[i], markersize=8)

plt.title('Monthly Sales Amount by Major Category (Jan-Apr 2015)', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=13)
plt.ylabel('Sales Amount (RMB)', fontsize=13)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
plt.tight_layout()
plt.savefig('/work/figure1_sales_trend.png', dpi=150)
plt.close()
print("Figure 1 saved")

# ========== FIGURE 2: Market share change ==========
df_pivot = df.pivot_table(index='Major_Category', columns='Month_Label', values='Monthly_Amount', aggfunc='sum')
df_pivot = df_pivot.fillna(0)
monthly_totals = df_pivot.sum()
share_df = df_pivot.div(monthly_totals, axis=1) * 100

top8_order = df.groupby('Major_Category')['Monthly_Amount'].sum().sort_values(ascending=False).head(8).index.tolist()
share_top8 = share_df.loc[share_df.index.isin(top8_order)]
other_share = 100 - share_top8.sum()
share_plot = share_top8.copy()
share_plot.loc['Other (7 categories)'] = other_share

plt.figure(figsize=(12, 8))
share_plot.T.plot(kind='bar', stacked=True, ax=plt.gca(), colormap='tab20', width=0.7)
plt.title('Monthly Market Share by Major Category (Jan-Apr 2015)', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=13)
plt.ylabel('Market Share (%)', fontsize=13)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('/work/figure2_market_share.png', dpi=150)
plt.close()
print("Figure 2 saved")

# ========== FIGURE 3: Growth rate heatmap ==========
df_growth = df.copy()
df_growth = df_growth.sort_values(['Major_Category', 'Sales_Month'])
df_growth['Prev_Amount'] = df_growth.groupby('Major_Category')['Monthly_Amount'].shift(1)
df_growth['Growth_Pct'] = ((df_growth['Monthly_Amount'] - df_growth['Prev_Amount']) / df_growth['Prev_Amount'] * 100)

growth_pivot = df_growth.pivot_table(index='Major_Category', columns='Month_Label', values='Growth_Pct', aggfunc='mean')
growth_pivot = growth_pivot.drop(columns=['Jan'], errors='ignore')
growth_pivot = growth_pivot.fillna(0)

plt.figure(figsize=(10, 10))
sns.heatmap(growth_pivot, annot=True, fmt='.1f', cmap='RdYlGn', center=0, 
            linewidths=1, cbar_kws={'label': 'Month-over-Month Growth (%)'})
plt.title('Month-over-Month Sales Growth Rate by Category (%)', fontsize=16, fontweight='bold')
plt.xlabel('Month Comparison', fontsize=13)
plt.ylabel('Major Category', fontsize=13)
plt.tight_layout()
plt.savefig('/work/figure3_growth_heatmap.png', dpi=150)
plt.close()
print("Figure 3 saved")

print("All figures saved successfully")
print("\nGrowth rates:")
print(growth_pivot.to_string())
print("\n\nTop 8 categories:", top8)