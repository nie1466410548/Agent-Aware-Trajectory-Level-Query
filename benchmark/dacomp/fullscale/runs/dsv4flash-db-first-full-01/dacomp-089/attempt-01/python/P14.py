import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('ggplot')
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

df = pd.read_csv('/work/final_risk_analysis.csv')

# ============================================================
# FIGURE A: Metric failure rates comparison by size segment
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# CDR pass rate
ax = axes[0]
cdr_pass = df.groupby('size_segment').apply(lambda x: (x['contact_density_ratio'] >= x['cdr_benchmark']).mean() * 100)
bars = ax.bar(cdr_pass.index, cdr_pass.values, color=['steelblue', 'darkorange'], edgecolor='black')
ax.set_ylim(0, 100)
ax.set_ylabel('Pass Rate (%)')
ax.set_title('Contact Density Pass Rate\n(Mid-Market: ≥5, Enterprise: ≥1.0)')
for bar, val in zip(bars, cdr_pass.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3, f'{val:.1f}%', ha='center', fontweight='bold')

# DMR pass rate
ax = axes[1]
dmr_pass = df[df['actual_contacts'] > 0].groupby('size_segment').apply(lambda x: (x['decision_maker_ratio'] >= 15).mean() * 100)
bars = ax.bar(dmr_pass.index, dmr_pass.values, color=['steelblue', 'darkorange'], edgecolor='black')
ax.set_ylim(0, 100)
ax.set_ylabel('Pass Rate (%)')
ax.set_title('Decision-Maker Ratio Pass Rate\n(Benchmark: ≥15%)')
for bar, val in zip(bars, dmr_pass.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3, f'{val:.1f}%', ha='center', fontweight='bold')

# Dept coverage pass rate
ax = axes[2]
dept_pass = df.groupby('size_segment').apply(lambda x: (x['dept_coverage'] >= 3).mean() * 100)
bars = ax.bar(dept_pass.index, dept_pass.values, color=['steelblue', 'darkorange'], edgecolor='black')
ax.set_ylim(0, 100)
ax.set_ylabel('Pass Rate (%)')
ax.set_title('Dept Coverage Pass Rate\n(Benchmark: ≥3 of 5 departments)')
for bar, val in zip(bars, dept_pass.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3, f'{val:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('/work/metric_fail_rates_by_size.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/metric_fail_rates_by_size.png")

# ============================================================
# FIGURE B: Risk category distribution by size
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
ct = pd.crosstab(df['size_segment'], df['risk_category'])
# Reorder columns
col_order = ['Low Risk', 'Medium Risk', 'High Risk', 'Critical']
ct = ct.reindex(columns=col_order)
ct.plot(kind='bar', stacked=True, ax=ax, color=['green', 'gold', 'orange', 'red'],
        edgecolor='black', alpha=0.8)
ax.set_ylabel('Number of Accounts')
ax.set_title('Risk Category Distribution by Customer Size Segment')
ax.set_xlabel('Size Segment')
plt.xticks(rotation=0)
for i, (idx, row) in enumerate(ct.iterrows()):
    total = row.sum()
    for j, (col, val) in enumerate(row.items()):
        if val > 0:
            y = row.iloc[:j].sum() + val / 2
            ax.text(i, y, f'{val}', ha='center', va='center', fontsize=9, fontweight='bold')
ax.legend(title='Risk Category', loc='upper right')
plt.tight_layout()
plt.savefig('/work/risk_by_size_stacked.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/risk_by_size_stacked.png")

# ============================================================
# FIGURE C: Top 10 highest-risk accounts (bar chart)
# ============================================================
top10 = df.nlargest(10, 'composite_risk')
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(top10['account_name'][::-1], top10['composite_risk'][::-1], 
               color=['crimson' if r == 'Critical' else 'orange' for r in top10['risk_category'][::-1]],
               edgecolor='black')
ax.axvline(65, color='black', linestyle='--', linewidth=1.5, label='Critical threshold (65)')
ax.set_xlabel('Composite Risk Score')
ax.set_title('Top 10 Highest-Risk Key Accounts')
ax.legend()
for bar, val in zip(bars, top10['composite_risk'][::-1]):
    ax.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.0f}', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('/work/top10_high_risk.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/top10_high_risk.png")

# ============================================================
# FIGURE D: Number of accounts requiring each action type
# ============================================================
fig, ax = plt.subplots(figsize=(10, 5))
actions = {
    'Establish baseline contacts\n(0 contacts)': (df['actual_contacts'] == 0).sum(),
    'Expand contact density\n(below benchmark)': ((df['actual_contacts'] > 0) & (df['contact_density_ratio'] < df['cdr_benchmark'])).sum(),
    'Add C-level / executive\ncontacts': (df['chief_count'] == 0).sum(),
    'Expand department\ncoverage (<3 depts)': (df['dept_coverage'] < 3).sum(),
    'Strategic account review\n(health score <40)': (df['customer_health_score'] < 40).sum()
}
colors = ['crimson', 'tomato', 'darkorange', 'gold', 'steelblue']
bars = ax.barh(list(actions.keys())[::-1], list(actions.values())[::-1], color=colors[::-1], edgecolor='black')
ax.set_xlabel('Number of Key Accounts')
ax.set_title('Action Plan Workload - Accounts Needing Each Intervention')
for bar, val in zip(bars, list(actions.values())[::-1]):
    ax.text(val + 10, bar.get_y() + bar.get_height()/2, f'{val}', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig('/work/action_workload.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/action_workload.png")

# Print final summary stats for report
print("\nFINAL SUMMARY STATISTICS")
print("=" * 60)
print(f"Key accounts: {len(df)}")
print(f"  Mid-Market: {(df['size_segment']=='Mid-Market').sum()} | Enterprise: {(df['size_segment']=='Enterprise').sum()}")
print(f"\nCDR benchmarks: Mid-Market 5.0, Enterprise 1.0")
print(f"  Pass rate overall: {(df['contact_density_ratio'] >= df['cdr_benchmark']).mean()*100:.1f}%")
print(f"  Zero contacts: {(df['actual_contacts']==0).mean()*100:.1f}%")
print(f"\nDMR benchmark: 15%")
print(f"  Pass rate (with contacts): {(df[df['actual_contacts']>0]['decision_maker_ratio']>=15).mean()*100:.1f}%")
print(f"\nDept coverage benchmark: 3+ of 5")
print(f"  Pass rate: {(df['dept_coverage']>=3).mean()*100:.1f}%")
print(f"\nRisk categories: Low {(df['risk_category']=='Low Risk').sum()} | Medium {(df['risk_category']=='Medium Risk').sum()} | High {(df['risk_category']=='High Risk').sum()} | Critical {(df['risk_category']=='Critical').sum()}")

print("\nFiles in /work:")
for f in sorted(os.listdir('/work')):
    print(f"  {f}")