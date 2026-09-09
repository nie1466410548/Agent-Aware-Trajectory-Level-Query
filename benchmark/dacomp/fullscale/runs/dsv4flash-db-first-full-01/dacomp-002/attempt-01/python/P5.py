import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read intermediate category data from S15
df = pd.read_json('/results/S15.rows.jsonl', lines=True)
df.columns = ['Major_Category', 'Intermediate_Category', 'Sales_Month', 'Monthly_Amount', 'Monthly_Qty']
df['Month'] = df['Sales_Month'].astype(str).str[4:6].astype(int)
df['Month_Label'] = df['Month'].map({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr'})

top_majors = ['Daily fresh products', 'Vegetables and fruits', 'Leisure', 'Grain and oil', 
              'Alcoholic beverages', 'Household & Personal Care', 'Meat and poultry', 'Instant mixes']

# Create a figure with subplots for each major category (4x2 grid)
fig, axes = plt.subplots(4, 2, figsize=(16, 22))
axes = axes.flatten()

for idx, major in enumerate(top_majors):
    ax = axes[idx]
    cat_df = df[df['Major_Category'] == major].copy()
    # Get top 5 intermediate categories by total amount for this major
    top_inter = cat_df.groupby('Intermediate_Category')['Monthly_Amount'].sum().sort_values(ascending=False).head(5).index.tolist()
    
    for inter in top_inter:
        inter_df = cat_df[cat_df['Intermediate_Category'] == inter].sort_values('Sales_Month')
        if len(inter_df) > 0:
            ax.plot(inter_df['Month_Label'], inter_df['Monthly_Amount'], marker='o', label=inter, linewidth=2)
    
    ax.set_title(major, fontsize=12, fontweight='bold')
    ax.legend(fontsize=7, loc='upper left')
    ax.set_ylabel('Sales Amount (RMB)')

plt.suptitle('Top 5 Intermediate Categories Monthly Sales by Major Category', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/figure4_intermediate_trends.png', dpi=150)
plt.close()
print("Figure 4 saved")

# Now print insights
print("\n=== Key Intermediate Category Trends ===")
for major in top_majors:
    cat_df = df[df['Major_Category'] == major].copy()
    top_inter = cat_df.groupby('Intermediate_Category')['Monthly_Amount'].sum().sort_values(ascending=False).head(3).index.tolist()
    print(f"\n{major}:")
    for inter in top_inter:
        inter_data = cat_df[cat_df['Intermediate_Category'] == inter].sort_values('Sales_Month')
        amounts = inter_data['Monthly_Amount'].values
        months = inter_data['Month_Label'].values
        if len(amounts) >= 2:
            change = ((amounts[-1] - amounts[0]) / amounts[0] * 100) if amounts[0] > 0 else 0
            trend = "upward" if change > 10 else ("downward" if change < -10 else "stable")
            print(f"  {inter}: {dict(zip(months, amounts.round(2)))} | Overall change: {change:.1f}% ({trend})")
        else:
            print(f"  {inter}: {dict(zip(months, amounts.round(2)))}")

# Also compute the overall category ranking changes
print("\n\n=== Category Ranking by Month (by Sales Amount) ===")
df['Rank'] = df.groupby('Sales_Month')['Monthly_Amount'].rank(ascending=False, method='dense')
rank_pivot = df.pivot_table(index='Major_Category', columns='Month_Label', values='Rank', aggfunc='mean')
print(rank_pivot.to_string())

# Monthly share of each major category
print("\n\n=== Monthly Share of Total Sales (% by Category) ===")
monthly_totals = df.groupby('Month_Label')['Monthly_Amount'].sum()
share_pivot = df.pivot_table(index='Major_Category', columns='Month_Label', values='Monthly_Amount', aggfunc='sum')
share_pct = share_pivot.div(monthly_totals, axis=1) * 100
print(share_pct.round(2).to_string())