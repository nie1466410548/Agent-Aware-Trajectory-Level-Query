import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/customer_health_scores.csv')

# Strategy matrix: health category x size segment
df['health_category'] = pd.cut(df['health_score'], bins=[0, 50, 80, 100], labels=['Low (<50)', 'Medium (50-80)', 'High (80+)'])
cat_order = ['Low (<50)', 'Medium (50-80)', 'High (80+)']
size_order = ['Small Business', 'Mid-Market', 'Large', 'Enterprise']

# Count matrix with annotation including % 
count_mat = pd.crosstab(df['health_category'], df['account_size_segment'])
count_mat = count_mat.reindex(index=cat_order, columns=size_order).fillna(0).astype(int)
total_per_seg = count_mat.sum(axis=0)

annot = count_mat.copy().astype(str)
for c in size_order:
    for r in cat_order:
        n = count_mat.loc[r, c]
        pct = n / total_per_seg[c] * 100 if total_per_seg[c] > 0 else 0
        annot.loc[r, c] = f"{n}\n({pct:.0f}%)"

plt.figure(figsize=(10, 4.5))
sns.heatmap(count_mat, annot=annot, fmt='', cmap='Blues', linewidths=1,
            cbar_kws={'label': 'Number of Accounts'})
plt.title('Account Distribution by Health Category and Size Segment\n(count and % of size segment)', fontsize=13, fontweight='bold')
plt.xlabel('Account Size Segment')
plt.ylabel('Health Category')
plt.tight_layout()
plt.savefig('/work/strategy_matrix.png', dpi=150)
plt.close()

# Also compute risk concentration table for report
print("Risk concentration by segment (Health<50 share of segment):")
low = df[df['health_score'] < 50]
tot = pd.crosstab(df['industry_normalized'], df['account_size_segment'])
lo = pd.crosstab(low['industry_normalized'], low['account_size_segment'])
for ind in lo.index:
    for seg in lo.columns:
        if tot.loc[ind, seg] > 0 and lo.loc[ind, seg] > 0:
            print(f"  {ind} | {seg}: {lo.loc[ind, seg]}/{tot.loc[ind, seg]} = {lo.loc[ind, seg]/tot.loc[ind, seg]*100:.1f}%")

print("\nTotal risk by size segment:")
for seg in size_order:
    n_tot = (df['account_size_segment']==seg).sum()
    n_low = (df[(df['account_size_segment']==seg)&(df['health_score']<50)]).shape[0]
    print(f"  {seg}: {n_low}/{n_tot} = {n_low/n_tot*100:.1f}%")

print("\nRevenue concentration:")
tier_sum = df.groupby('revenue_tier', observed=False)['predicted_6mo_revenue'].sum()
total = df['predicted_6mo_revenue'].sum()
for t in ['Tier 1 (Highest)','Tier 2','Tier 3','Tier 4','Tier 5 (Lowest)']:
    print(f"  {t}: {tier_sum[t]/1e9:.1f}B ({tier_sum[t]/total*100:.1f}%)")
print(f"\nTotal predicted 6-month: {total/1e9:.0f}B")