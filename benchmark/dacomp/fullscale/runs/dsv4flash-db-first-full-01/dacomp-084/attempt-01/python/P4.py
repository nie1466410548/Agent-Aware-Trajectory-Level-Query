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
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate
FROM workday__organization_overview
""")
ov_df = db.frame(ov)
tier_order = ['Small (0-30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (300+)']
ov_df['organization_size_category'] = pd.Categorical(ov_df['organization_size_category'], categories=tier_order, ordered=True)

# Create management ratio bins per tier
# Use tier-specific bins based on data distribution
def assign_mr_bin(row):
    mr = row['management_ratio']
    sz = row['organization_size_category']
    if sz == 'Small (0-30)':
        if mr < 0.15: return '<0.15'
        elif mr < 0.18: return '0.15-0.18'
        elif mr < 0.21: return '0.18-0.21'
        else: return '>=0.21'
    elif sz == 'Medium (30-120)':
        if mr < 0.15: return '<0.15'
        elif mr < 0.18: return '0.15-0.18'
        else: return '>=0.18'
    elif sz == 'Large (120-300)':
        if mr < 0.18: return '<0.18'
        elif mr < 0.21: return '0.18-0.21'
        else: return '>=0.21'
    else:  # XL
        if mr < 0.21: return '<0.21'
        elif mr < 0.25: return '0.21-0.25'
        else: return '>=0.25'

ov_df['mr_bin'] = ov_df.apply(assign_mr_bin, axis=1)

# Group by tier and mr_bin
results = ov_df.groupby(['organization_size_category','mr_bin'], observed=True).agg(
    n=('organization_id','count'),
    avg_health=('organization_health_score','mean'),
    avg_perf=('avg_employee_performance_score','mean'),
    avg_fill=('position_fill_rate','mean'),
    avg_turnover=('annual_turnover_rate','mean')
).round(3)
print("=== Management Ratio Bins: Performance by Tier ===")
print(results.to_string())

# Save
results.to_csv('mr_bin_analysis.csv')

# Create a dashboard figure
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
tiers = ['Small (0-30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (300+)']
metrics = ['avg_health', 'avg_perf', 'avg_fill', 'avg_turnover']
metric_labels = ['Avg Health Score', 'Avg Perf Score', 'Avg Fill Rate', 'Avg Turnover Rate']

for i, tier in enumerate(tiers):
    ax = axes[i//2, i%2]
    tdata = results.loc[tier].reset_index()
    x = np.arange(len(tdata))
    width = 0.2
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
    for j, (m, lbl) in enumerate(zip(metrics, metric_labels)):
        ax.bar(x + j*width, tdata[m].values, width, label=lbl, color=colors[j])
    ax.set_xticks(x + width*1.5)
    ax.set_xticklabels(tdata['mr_bin'], fontsize=9)
    ax.set_title(f'{tier}', fontsize=11)
    ax.legend(fontsize=7, bbox_to_anchor=(1.02,1), loc='upper left')

plt.tight_layout()
plt.savefig('mr_bin_analysis.png', dpi=110)
print("Saved mr_bin_analysis.png")

# Also compute employees per manager (staffing density)
ov_df['employees_per_manager'] = 1 / ov_df['management_ratio']
density = ov_df.groupby('organization_size_category', observed=True)['employees_per_manager'].agg(['mean','std','min','max']).round(1)
print("\n=== Staffing Density (employees per manager) ===")
print(density)
density.to_csv('staffing_density.csv')