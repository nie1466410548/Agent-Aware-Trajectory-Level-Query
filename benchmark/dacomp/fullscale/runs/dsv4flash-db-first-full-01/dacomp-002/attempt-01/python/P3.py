import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read intermediate category monthly data
df = pd.read_json('/results/S15.rows.jsonl', lines=True)
df.columns = ['Major_Category', 'Intermediate_Category', 'Sales_Month', 'Monthly_Amount', 'Monthly_Qty']
df['Month'] = df['Sales_Month'].astype(str).str[4:6].astype(int)
df['Month_Label'] = df['Month'].map({1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr'})

# For each major category, find the top intermediate categories and their trends
top_majors = ['Daily fresh products', 'Vegetables and fruits', 'Leisure', 'Grain and oil', 
              'Alcoholic beverages', 'Household & Personal Care', 'Meat and poultry', 'Instant mixes']

# Create a figure with subplots for each major category
fig, axes = plt.subplots(4, 2, figsize=(16, 20))
axes = axes.flatten()

for idx, major in enumerate(top_majors):
    ax = axes[idx]
    cat_df = df[df['Major_Category'] == major].copy()
    # Get top 5 intermediate categories by total amount
    top_inter = cat_df.groupby('Intermediate_Category')['Monthly_Amount'].sum().sort_values(ascending=False).head(5).index.tolist()
    
    for inter in top_inter:
        inter_df = cat_df[cat_df['Intermediate_Category'] == inter].sort_values('Sales_Month')
        ax.plot(inter_df['Month_Label'], inter_df['Monthly_Amount'], marker='o', label=inter, linewidth=2)
    
    ax.set_title(major, fontsize=12, fontweight='bold')
    ax.legend(fontsize=7, loc='upper left')
    ax.set_ylabel('Sales Amount (RMB)')

plt.suptitle('Top 5 Intermediate Categories Monthly Sales by Major Category', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/figure4_intermediate_trends.png', dpi=150)
plt.close()
print("Figure 4 saved")

# ========== FIGURE 5: Promotional mix by category ==========
# Read promotional data
df_full = pd.read_json('/results/S1.rows.jsonl', lines=True)
df_full.columns = ['Customer_ID','Major_Cat_Code','Major_Cat_Name','Inter_Cat_Code','Inter_Cat_Name',
                   'Minor_Cat_Code','Minor_Cat_Name','Sales_Date','Sales_Month','Product_Code',
                   'Spec_Model','Product_Type','Unit','Sales_Qty','Sales_Amount','Is_Promotional']

# Promotional mix by major category
promo_by_cat = df_full.groupby(['Major_Cat_Name', 'Is_Promotional']).agg(
    total_amount=('Sales_Amount', 'sum'),
    trans_count=('Customer_ID', 'count')
).reset_index()

# Pivot for heatmap
promo_pivot = promo_by_cat.pivot_table(index='Major_Cat_Name', columns='Is_Promotional', values='total_amount', aggfunc='sum').fillna(0)
promo_pct = promo_pivot.div(promo_pivot.sum(axis=1), axis=0) * 100

# Only show top categories
top_cats = df_full.groupby('Major_Cat_Name')['Sales_Amount'].sum().sort_values(ascending=False).head(10).index.tolist()
promo_pct_top = promo_pct.loc[promo_pct.index.isin(top_cats)]

plt.figure(figsize=(12, 8))
sns.heatmap(promo_pct_top, annot=True, fmt='.1f', cmap='YlOrRd', linewidths=1)
plt.title('Promotional Mix as % of Sales Amount by Major Category', fontsize=16, fontweight='bold')
plt.ylabel('Major Category', fontsize=13)
plt.xlabel('Promotion Type', fontsize=13)
plt.tight_layout()
plt.savefig('/work/figure5_promotional_mix.png', dpi=150)
plt.close()
print("Figure 5 saved")

# Print key insights
print("\n=== Key Intermediate Category Trends ===")
for major in top_majors:
    cat_df = df[df['Major_Category'] == major].copy()
    top_inter = cat_df.groupby('Intermediate_Category')['Monthly_Amount'].sum().sort_values(ascending=False).head(3).index.tolist()
    print(f"\n{major}:")
    for inter in top_inter:
        inter_data = cat_df[cat_df['Intermediate_Category'] == inter].sort_values('Sales_Month')
        amounts = inter_data['Monthly_Amount'].values
        months = inter_data['Month_Label'].values
        trend = "up" if len(amounts) >= 4 and amounts[-1] > amounts[0] else ("down" if len(amounts) >= 4 and amounts[-1] < amounts[0] else "mixed")
        print(f"  {inter}: {dict(zip(months, amounts.round(2)))} - {trend}")

print("\n\n=== Promotional Insights ===")
print(promo_pct_top.to_string())