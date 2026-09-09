import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Pull data for final comprehensive figure
ov = db.query("""
SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate
FROM workday__organization_overview
""")
ov_df = db.frame(ov)
tier_order = ['Small (0-30)', 'Medium (30-120)', 'Large (120-300)', 'Extra Large (300+)']
ov_df['organization_size_category'] = pd.Categorical(ov_df['organization_size_category'], categories=tier_order, ordered=True)

# Create a comprehensive figure with 4 panels
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Management ratio vs Health score, colored by tier
ax = axes[0,0]
colors = {'Small (0-30)': '#2ecc71', 'Medium (30-120)': '#3498db', 'Large (120-300)': '#f39c12', 'Extra Large (300+)': '#e74c3c'}
for tier in tier_order:
    tdf = ov_df[ov_df['organization_size_category']==tier]
    ax.scatter(tdf['management_ratio'], tdf['organization_health_score'], 
               c=colors[tier], label=tier, s=50, alpha=0.7)
ax.set_xlabel('Management Ratio')
ax.set_ylabel('Organization Health Score')
ax.set_title('Management Ratio vs Health Score')
ax.legend(fontsize=8)

# Add optimal region annotations
# Small: <0.15 is best; Medium: 0.15-0.18; Large: 0.18-0.21; XL: 0.21-0.25
ax.axvspan(0.1, 0.15, alpha=0.1, color='#2ecc71', label='_nolegend_')
ax.axvspan(0.15, 0.18, alpha=0.1, color='#3498db', label='_nolegend_')
ax.axvspan(0.18, 0.21, alpha=0.1, color='#f39c12', label='_nolegend_')
ax.axvspan(0.21, 0.25, alpha=0.1, color='#e74c3c', label='_nolegend_')

# Panel 2: Management ratio histogram by tier
ax = axes[0,1]
for tier in tier_order:
    tdf = ov_df[ov_df['organization_size_category']==tier]
    ax.hist(tdf['management_ratio'], bins=8, alpha=0.5, label=tier, color=colors[tier])
ax.set_xlabel('Management Ratio')
ax.set_ylabel('Count')
ax.set_title('Management Ratio Distribution by Tier')
ax.legend(fontsize=8)

# Panel 3: Performance score vs fill rate, colored by management ratio bin
ax = axes[1,0]
sc = ax.scatter(ov_df['position_fill_rate'], ov_df['avg_employee_performance_score'],
                c=ov_df['management_ratio'], cmap='viridis', s=50, alpha=0.7)
ax.set_xlabel('Position Fill Rate')
ax.set_ylabel('Avg Employee Performance Score')
ax.set_title('Fill Rate vs Performance Score (colored by Mgmt Ratio)')
plt.colorbar(sc, ax=ax, label='Management Ratio')

# Panel 4: Turnover vs health score
ax = axes[1,1]
for tier in tier_order:
    tdf = ov_df[ov_df['organization_size_category']==tier]
    ax.scatter(tdf['annual_turnover_rate'], tdf['organization_health_score'],
               c=colors[tier], label=tier, s=50, alpha=0.7)
ax.set_xlabel('Annual Turnover Rate')
ax.set_ylabel('Organization Health Score')
ax.set_title('Turnover Rate vs Health Score')
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig('comprehensive_analysis.png', dpi=120)
print("Saved comprehensive_analysis.png")

# Compute optimal management ratio recommendations
print("\n=== Optimal Management Ratio Recommendations ===")
for tier in tier_order:
    tdf = ov_df[ov_df['organization_size_category']==tier]
    # Best bin based on health score
    tdf['mr_bin'] = pd.cut(tdf['management_ratio'], bins=5)
    bin_stats = tdf.groupby('mr_bin', observed=True).agg(
        n=('organization_health_score','count'),
        avg_health=('organization_health_score','mean'),
        avg_perf=('avg_employee_performance_score','mean'),
        avg_fill=('position_fill_rate','mean'),
        avg_turnover=('annual_turnover_rate','mean')
    ).round(3)
    best_bin = bin_stats.loc[bin_stats['avg_health'].idxmax()]
    print(f"\n{tier}:")
    print(f"  Best bin: {best_bin.name}")
    print(f"  n={best_bin['n']}, avg_health={best_bin['avg_health']}, avg_perf={best_bin['avg_perf']}")
    print(f"  avg_fill={best_bin['avg_fill']}, avg_turnover={best_bin['avg_turnover']}")
    print(f"  Staffing density (emp/manager): {1/best_bin.name.mid:.1f}")