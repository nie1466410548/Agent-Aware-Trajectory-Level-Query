import json, pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load data
rows = []
with open('/results/S19.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
rep_df = pd.DataFrame(rows)
rep_df.columns = ['owner_id', 'rep_name', 'manager_id', 'workload_score', 'efficiency_score',
                  'num_customers', 'total_annual_revenue', 'coverage_rate_capped',
                  'distinct_states', 'distinct_cities', 'win_rate', 'avg_deal_size_usd',
                  'avg_sales_cycle_days', 'opp_conversion_rate']
rep_df['efficiency_score'] = rep_df['efficiency_score'].fillna(rep_df['efficiency_score'].median())

fw = pd.read_csv('/work/final_workloads.csv', index_col=0)
baseline_ws = rep_df.set_index('owner_id')['workload_score']
final_ws = fw['workload']

avg_ws = baseline_ws.mean()
lower_target = avg_ws * 0.85
upper_target = avg_ws * 1.15

# Figure 1: Histogram
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
ax.hist(baseline_ws, bins=30, alpha=0.7, color='coral', edgecolor='black')
ax.axvline(lower_target, color='red', linestyle='--', label=f'±15% bounds ({lower_target:.1f}, {upper_target:.1f})')
ax.axvline(upper_target, color='red', linestyle='--')
ax.axvline(avg_ws, color='blue', linestyle='-', label=f'Mean: {avg_ws:.2f}')
ax.set_xlabel('Workload Score')
ax.set_ylabel('Number of Reps')
ax.set_title('Baseline Workload Distribution')
ax.legend(fontsize=8)
ax.text(0.95, 0.95, f'Std: {baseline_ws.std():.2f}\nIn range: 347/1000', 
        transform=ax.transAxes, va='top', ha='right', fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax = axes[1]
ax.hist(final_ws, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
ax.axvline(lower_target, color='red', linestyle='--', label=f'±15% bounds')
ax.axvline(upper_target, color='red', linestyle='--')
ax.axvline(avg_ws, color='blue', linestyle='-', label=f'Target Mean: {avg_ws:.2f}')
ax.set_xlabel('Workload Score')
ax.set_ylabel('Number of Reps')
ax.set_title('After Reallocation Workload Distribution')
ax.legend(fontsize=8)
ax.text(0.95, 0.95, f'Std: {final_ws.std():.2f}\nIn range: 907/1000', 
        transform=ax.transAxes, va='top', ha='right', fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('/work/workload_comparison.png', dpi=150)
plt.close()

# Figure 2: Before/after scatter
fig, ax = plt.subplots(figsize=(8, 8))
common = baseline_ws.index.intersection(final_ws.index)
ax.scatter(baseline_ws[common], final_ws[common], alpha=0.3, s=10)
ax.plot([0, 25], [0, 25], 'k--', alpha=0.5, label='y=x')
ax.axhline(lower_target, color='red', linestyle=':', alpha=0.5)
ax.axhline(upper_target, color='red', linestyle=':', alpha=0.5)
ax.axvline(lower_target, color='red', linestyle=':', alpha=0.5)
ax.axvline(upper_target, color='red', linestyle=':', alpha=0.5)
ax.set_xlabel('Baseline Workload Score')
ax.set_ylabel('Final Workload Score')
ax.set_title('Workload Score: Before vs After Reallocation')
ax.legend()
plt.tight_layout()
plt.savefig('/work/workload_scatter.png', dpi=150)
plt.close()

# Figure 3: Industry compliance
baseline_comp = pd.read_csv('/work/baseline_compliance.csv', header=None, index_col=0, squeeze=True)
final_comp = pd.read_csv('/work/final_compliance_series.csv', index_col=0, header=None, squeeze=True)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(baseline_comp, bins=20, alpha=0.7, color='coral', edgecolor='black')
axes[0].axvline(0.6, color='green', linestyle='--', linewidth=2, label='60% threshold')
axes[0].set_xlabel('% in Top 3 Industries')
axes[0].set_ylabel('Number of Reps')
axes[0].set_title(f'Baseline Industry Compliance\n{(baseline_comp >= 0.6).sum()}/1000 reps meet 60% rule')
axes[0].legend()

axes[1].hist(final_comp, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
axes[1].axvline(0.6, color='green', linestyle='--', linewidth=2, label='60% threshold')
axes[1].set_xlabel('% in Top 3 Industries')
axes[1].set_ylabel('Number of Reps')
axes[1].set_title(f'Final Industry Compliance\n{(final_comp >= 0.6).sum()}/1000 reps meet 60% rule')
axes[1].legend()

plt.tight_layout()
plt.savefig('/work/industry_compliance.png', dpi=150)
plt.close()

print("Visualizations saved.")
print("Files:", ['/work/workload_comparison.png', '/work/workload_scatter.png', '/work/industry_compliance.png'])