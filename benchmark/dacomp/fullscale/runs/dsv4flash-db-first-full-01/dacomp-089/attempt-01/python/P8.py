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
plt.rcParams['figure.figsize'] = (12, 8)

columns = [
    'account_id', 'account_name', 'annual_revenue', 'number_of_employees', 'total_contacts',
    'industry_normalized', 'account_size_segment', 'company_size_category', 'churn_risk_level',
    'customer_health_score', 'relationship_strength', 'actual_contacts', 'chief_count',
    'has_sales', 'has_finance', 'has_operations', 'has_it', 'has_hr', 'distinct_depts',
    'contact_density_ratio', 'decision_maker_ratio', 'dept_coverage'
]

rows = []
with open('/results/S40.rows.jsonl', 'r') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows, columns=columns)
df['contact_density_ratio'] = df['contact_density_ratio'].fillna(0)

df['cdr_risk'] = np.where(
    df['contact_density_ratio'] < 5.0, 
    100 * (1 - np.minimum(df['contact_density_ratio'] / 5.0, 1.0)),
    np.where(df['contact_density_ratio'] < 15.0, 50, 0)
).clip(0, 100)

df['dmr_risk'] = np.where(
    df['actual_contacts'] == 0, 100,
    np.where(df['decision_maker_ratio'] < 15.0,
             100 * (1 - df['decision_maker_ratio'] / 15.0),
             0)
).clip(0, 100)

df['dept_risk'] = 100 * (1 - df['dept_coverage'] / 5.0)
df['health_risk'] = 100 * (1 - df['customer_health_score'] / 100.0)
df['composite_risk'] = (0.30 * df['cdr_risk'] + 0.25 * df['dmr_risk'] + 
                         0.25 * df['dept_risk'] + 0.20 * df['health_risk'])
df['risk_category'] = pd.cut(df['composite_risk'], bins=[0, 30, 50, 70, 100],
                              labels=['Low', 'Medium', 'High', 'Critical'])

# ============================================================
# FIGURE 2: Industry Heatmap - Risk Profiles
# ============================================================
industry_metrics = df.groupby('industry_normalized').agg({
    'contact_density_ratio': 'mean',
    'decision_maker_ratio': 'mean',
    'dept_coverage': 'mean',
    'composite_risk': 'mean',
    'customer_health_score': 'mean'
}).round(2)

fig, ax = plt.subplots(figsize=(14, 10))
risk_metrics = industry_metrics[['contact_density_ratio', 'decision_maker_ratio', 
                                  'dept_coverage', 'composite_risk', 'customer_health_score']]
# Manual z-score normalization
risk_scaled = (risk_metrics - risk_metrics.mean()) / risk_metrics.std()

sns.heatmap(risk_scaled, annot=risk_metrics.round(1), fmt='.1f', cmap='RdYlGn_r', 
            center=0, linewidths=1, ax=ax, cbar_kws={'label': 'Z-score'})
ax.set_title('Industry Risk Profile Heatmap', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/industry_risk_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/industry_risk_heatmap.png")

# ============================================================
# FIGURE 3: Risk Component Breakdown for Top 30 High-Risk Accounts
# ============================================================
top_risk = df.nlargest(30, 'composite_risk')
fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(top_risk))
width = 0.2

ax.bar(x - 1.5*width, top_risk['cdr_risk'].values, width, label='Contact Density Risk', color='steelblue')
ax.bar(x - 0.5*width, top_risk['dmr_risk'].values, width, label='Decision-Maker Risk', color='forestgreen')
ax.bar(x + 0.5*width, top_risk['dept_risk'].values, width, label='Department Coverage Risk', color='darkorange')
ax.bar(x + 1.5*width, top_risk['health_risk'].values, width, label='Health Score Risk', color='crimson')

ax.set_xlabel('Account (Top 30 by Risk)')
ax.set_ylabel('Risk Score (0-100)')
ax.set_title('Risk Component Breakdown - Top 30 High-Risk Accounts')
ax.set_xticks(x)
ax.set_xticklabels([n[:12] + '..' if len(n) > 12 else n for n in top_risk['account_name']], 
                   rotation=45, ha='right', fontsize=8)
ax.legend(loc='upper right')
ax.set_ylim(0, 110)
plt.tight_layout()
plt.savefig('/work/risk_breakdown_top30.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/risk_breakdown_top30.png")

# ============================================================
# FIGURE 4: Scatter - Contact Density vs Decision Maker Ratio
# ============================================================
fig, ax = plt.subplots(figsize=(12, 8))
scatter = ax.scatter(
    df['contact_density_ratio'].clip(0, 100), 
    df['decision_maker_ratio'].clip(0, 50),
    c=df['composite_risk'], cmap='RdYlGn_r', alpha=0.6, s=30, edgecolors='black', linewidth=0.5
)
ax.axhline(15, color='red', linestyle='--', linewidth=2, label='DMR Benchmark (15%)')
ax.axvline(5, color='red', linestyle='--', linewidth=2, label='CDR Benchmark (5.0)')
ax.set_xlabel('Contact Density Ratio (Contacts/Employees * 1000)')
ax.set_ylabel('Decision Maker Ratio (%)')
ax.set_title('Risk Assessment Matrix: Contact Density vs Decision-Maker Ratio')
ax.set_xlim(0, 100)
ax.set_ylim(0, 50)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Composite Risk Score', rotation=270, labelpad=15)
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig('/work/risk_matrix_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/risk_matrix_scatter.png")

# ============================================================
# FIGURE 5: Company Size Comparison
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

ax = axes[0]
for sz in ['Enterprise', 'Mid-Market']:
    subset = df[df['company_size_category'] == sz]
    ax.hist(subset['contact_density_ratio'].clip(0, 50), bins=20, alpha=0.5, label=sz)
ax.axvline(5, color='red', linestyle='--', linewidth=1.5)
ax.set_xlabel('Contact Density Ratio')
ax.set_ylabel('Frequency')
ax.set_title('CDR by Company Size')
ax.legend()

ax = axes[1]
for sz in ['Enterprise', 'Mid-Market']:
    subset = df[(df['company_size_category'] == sz) & (df['actual_contacts'] > 0)]
    ax.hist(subset['decision_maker_ratio'].clip(0, 30), bins=15, alpha=0.5, label=sz)
ax.axvline(15, color='red', linestyle='--', linewidth=1.5)
ax.set_xlabel('Decision Maker Ratio (%)')
ax.set_ylabel('Frequency')
ax.set_title('DMR by Company Size')
ax.legend()

ax = axes[2]
size_dept = df.groupby('company_size_category')['dept_coverage'].mean()
ax.bar(size_dept.index, size_dept.values, color=['steelblue', 'darkorange'], edgecolor='black')
ax.set_ylabel('Average Dept Coverage')
ax.set_title('Avg Dept Coverage by Company Size')
for i, v in enumerate(size_dept.values):
    ax.text(i, v + 0.02, f'{v:.2f}', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('/work/company_size_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/company_size_comparison.png")

# ============================================================
# FIGURE 6: Department coverage heatmap by industry
# ============================================================
dept_cols = ['has_sales', 'has_finance', 'has_operations', 'has_it', 'has_hr']
dept_by_industry = df.groupby('industry_normalized')[dept_cols].mean().round(3)
dept_by_industry.columns = ['Sales', 'Finance', 'Operations', 'IT', 'HR']

fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(dept_by_industry, annot=True, fmt='.2f', cmap='YlOrRd', linewidths=1, ax=ax,
            cbar_kws={'label': 'Coverage Proportion'})
ax.set_title('Department Coverage by Industry', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/dept_coverage_by_industry.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/dept_coverage_by_industry.png")

print("\nAll visualizations saved!")
print(f"Files in /work: {sorted(os.listdir('/work'))}")