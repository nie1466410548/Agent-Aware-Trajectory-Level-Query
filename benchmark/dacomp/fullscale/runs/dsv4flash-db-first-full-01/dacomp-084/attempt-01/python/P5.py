import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Pull data
ov = db.query("""
SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate,
       organization_type, staffing_model, organization_maturity_level
FROM workday__organization_overview
""")
ov_df = db.frame(ov)
tier_order = ['Small (0-30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (300+)']
ov_df['organization_size_category'] = pd.Categorical(ov_df['organization_size_category'], categories=tier_order, ordered=True)

# Identify top 10% per tier
ov_df['rn'] = ov_df.groupby('organization_size_category', observed=True)['organization_health_score'].rank(method='first', ascending=False)
ov_df['n'] = ov_df.groupby('organization_size_category', observed=True)['organization_id'].transform('count')
ov_df['top10'] = ov_df['rn'] <= np.ceil(ov_df['n'] * 0.1)

# Top 10% summary per tier
top10 = ov_df[ov_df['top10']].groupby('organization_size_category', observed=True).agg(
    n=('organization_id','count'),
    avg_health=('organization_health_score','mean'),
    avg_mr=('management_ratio','mean'),
    avg_perf=('avg_employee_performance_score','mean'),
    avg_fill=('position_fill_rate','mean'),
    avg_turnover=('annual_turnover_rate','mean'),
    avg_emp=('current_active_employees','mean')
).round(3)
print("=== Top 10% Performing Organizations Per Tier ===")
print(top10.to_string())

rest = ov_df[~ov_df['top10']].groupby('organization_size_category', observed=True).agg(
    n=('organization_id','count'),
    avg_health=('organization_health_score','mean'),
    avg_mr=('management_ratio','mean'),
    avg_perf=('avg_employee_performance_score','mean'),
    avg_fill=('position_fill_rate','mean'),
    avg_turnover=('annual_turnover_rate','mean')
).round(3)
print("\n=== Rest of Organizations Per Tier ===")
print(rest.to_string())

# Create comparison figure
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
metrics = ['avg_health', 'avg_mr', 'avg_perf', 'avg_fill', 'avg_turnover']
labels = ['Health Score', 'Management Ratio', 'Perf Score', 'Fill Rate', 'Turnover Rate']
tiers = ['Small (0-30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (300+)']

# Comparison bar chart
x = np.arange(len(tiers))
width = 0.35
for idx, (metric, lbl) in enumerate(zip(metrics[:4], labels[:4])):
    ax = axes[idx//2, idx%2]
    top_vals = top10[metric].values if metric in top10.columns else None
    rest_vals = rest[metric].values if metric in rest.columns else None
    if top_vals is not None:
        ax.bar(x - width/2, top_vals, width, label='Top 10%', color='#2ecc71')
    if rest_vals is not None:
        ax.bar(x + width/2, rest_vals, width, label='Rest', color='#e74c3c')
    ax.set_xticks(x)
    ax.set_xticklabels([t.split(' ')[0] for t in tiers], fontsize=9)
    ax.set_title(lbl, fontsize=11)
    ax.legend(fontsize=8)

# Turnover
ax = axes[1,1]
ax.bar(x - width/2, top10['avg_turnover'].values, width, label='Top 10%', color='#2ecc71')
ax.bar(x + width/2, rest['avg_turnover'].values, width, label='Rest', color='#e74c3c')
ax.set_xticks(x)
ax.set_xticklabels([t.split(' ')[0] for t in tiers], fontsize=9)
ax.set_title('Turnover Rate', fontsize=11)
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig('top10_vs_rest.png', dpi=110)
print("Saved top10_vs_rest.png")

# Detailed individual top 10% orgs
top10_detail = ov_df[ov_df['top10']][['organization_id','organization_size_category',
    'organization_name','current_active_employees','organization_health_score',
    'performance_category','management_ratio','avg_employee_performance_score',
    'position_fill_rate','annual_turnover_rate','organization_type','staffing_model',
    'organization_maturity_level']].sort_values(['organization_size_category','organization_health_score'], ascending=[True,False])
top10_detail.to_csv('top10_detail.csv', index=False)
print("\nSaved top10_detail.csv")

# Print top 10% orgs
print("\n=== Top 10% Organizations Details ===")
print(top10_detail.to_string())