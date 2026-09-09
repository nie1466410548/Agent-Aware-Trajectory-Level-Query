import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Final recommendations table construction
recs = pd.DataFrame({
    'Tier': ['Small (<30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (>300)'],
    'N_orgs': [46, 35, 21, 16],
    'Avg_Health': [67.3, 65.5, 65.5, 66.8],
    'Optimal_MR_range': ['0.14-0.20', '0.15-0.18', '0.18-0.23', '0.21-0.25'],
    'Optimal_MR_mid': [0.17, 0.165, 0.205, 0.23],
    'Emp_per_manager': ['5.0-7.1 (lean ~5-7)', '5.6-6.7', '4.3-5.6', '4.0-4.8'],
    'Min_fill_rate_target': [0.92, 0.92, 0.93, 0.93],
    'Max_turnover_target': [0.15, 0.15, 0.15, 0.15],
})
print(recs.to_string())

# Figure: Recommended management ratio ranges by tier
fig, ax = plt.subplots(figsize=(9, 5))
tiers = recs['Tier'].tolist()
mids = recs['Optimal_MR_mid'].tolist()
lo = [0.14, 0.15, 0.18, 0.21]
hi = [0.20, 0.18, 0.23, 0.25]

for i, tier in enumerate(tiers):
    ax.barh(tier, hi[i]-lo[i], left=lo[i], height=0.5, color='#2ecc71', alpha=0.8)
    ax.text(mids[i], i, f'{lo[i]:.2f}-{hi[i]:.2f}', ha='center', va='center', fontsize=10, fontweight='bold')

ax.set_xlabel('Management Ratio (managers / total employees)')
ax.set_title('Recommended Optimal Management Ratio Ranges by Size Tier')
ax.set_xlim(0.12, 0.27)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('recommendation_mr_ranges.png', dpi=120)
print("Saved recommendation_mr_ranges.png")

recs.to_csv('recommendations.csv', index=False)

# Verify thresholds in top10 vs rest: fill rate and turnover distributions
ov = db.query("""
SELECT organization_id, organization_size_category, organization_health_score,
       position_fill_rate, annual_turnover_rate, avg_employee_performance_score
FROM workday__organization_overview
""")
ov_df = db.frame(ov)
tier_order = ['Small (0-30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (300+)']
ov_df['organization_size_category'] = pd.Categorical(ov_df['organization_size_category'], categories=tier_order, ordered=True)
ov_df['rn'] = ov_df.groupby('organization_size_category', observed=True)['organization_health_score'].rank(method='first', ascending=False)
ov_df['n'] = ov_df.groupby('organization_size_category', observed=True)['organization_id'].transform('count')
ov_df['top10'] = ov_df['rn'] <= np.ceil(ov_df['n']*0.1)

print("\nTop10 fill rate stats:", ov_df[ov_df['top10']]['position_fill_rate'].describe().round(3).to_dict())
print("Top10 turnover stats:", ov_df[ov_df['top10']]['annual_turnover_rate'].describe().round(3).to_dict())
print("Top10 perf stats:", ov_df[ov_df['top10']]['avg_employee_performance_score'].describe().round(3).to_dict())
print("\nRest fill rate stats:", ov_df[~ov_df['top10']]['position_fill_rate'].describe().round(3).to_dict())
print("Rest turnover stats:", ov_df[~ov_df['top10']]['annual_turnover_rate'].describe().round(3).to_dict())
print("Rest perf stats:", ov_df[~ov_df['top10']]['avg_employee_performance_score'].describe().round(3).to_dict())