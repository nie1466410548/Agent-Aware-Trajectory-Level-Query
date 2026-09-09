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

# Load the updated data
columns = [
    'account_id', 'account_name', 'annual_revenue', 'number_of_employees', 'industry_normalized',
    'company_size_category', 'customer_health_score', 'actual_contacts', 'chief_count',
    'has_sales', 'has_finance', 'has_operations', 'has_it', 'has_hr',
    'dept_coverage', 'contact_density_ratio', 'decision_maker_ratio'
]

rows = []
with open('/results/S43.rows.jsonl', 'r') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows, columns=columns)
df['contact_density_ratio'] = df['contact_density_ratio'].fillna(0)

print("Department Coverage Stats (with Engineering as IT proxy):")
print(f"  Mean: {df['dept_coverage'].mean():.2f}")
print(f"  Median: {df['dept_coverage'].median():.2f}")
print(f"  Coverage distribution:")
for i in range(6):
    cnt = (df['dept_coverage'] == i).sum()
    print(f"    {i}/5 departments: {cnt} ({cnt/len(df)*100:.1f}%)")

print(f"\nIndividual department coverage:")
for dept in ['has_sales', 'has_finance', 'has_operations', 'has_it', 'has_hr']:
    cnt = (df[dept] == 1).sum()
    print(f"  {dept.replace('has_', '')}: {cnt} ({cnt/len(df)*100:.1f}%)")

# Accounts with all 5 departments
all5 = (df['dept_coverage'] == 5).sum()
print(f"\nAccounts with all 5 departments: {all5}")

# Accounts with 3+ departments
ge3 = (df['dept_coverage'] >= 3).sum()
print(f"Accounts with 3+ departments: {ge3} ({ge3/len(df)*100:.1f}%)")

# Recompute risk scores
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

print(f"\nUpdated Risk Distribution:")
for cat in ['Low', 'Medium', 'High', 'Critical']:
    cnt = (df['risk_category'] == cat).sum()
    print(f"  {cat}: {cnt} ({cnt/len(df)*100:.1f}%)")

print(f"\nComposite Risk Score Stats:")
print(f"  Mean: {df['composite_risk'].mean():.2f}")
print(f"  Median: {df['composite_risk'].median():.2f}")

# Update visualization: Dept coverage heatmap
dept_cols = ['has_sales', 'has_finance', 'has_operations', 'has_it', 'has_hr']
dept_by_industry = df.groupby('industry_normalized')[dept_cols].mean().round(3)
dept_by_industry.columns = ['Sales', 'Finance', 'Operations', 'IT/Engineering', 'HR']

fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(dept_by_industry, annot=True, fmt='.2f', cmap='YlOrRd', linewidths=1, ax=ax,
            cbar_kws={'label': 'Coverage Proportion'})
ax.set_title('Department Coverage by Industry (Engineering mapped to IT)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/dept_coverage_by_industry_v2.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/dept_coverage_by_industry_v2.png")

# Update risk distribution figure
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Contact Density
ax = axes[0, 0]
cdr_vals = df['contact_density_ratio'].clip(0, 100)
ax.hist(cdr_vals, bins=50, color='steelblue', edgecolor='white', alpha=0.7)
ax.axvline(5.0, color='red', linestyle='--', linewidth=2, label='Benchmark (5.0)')
ax.set_xlabel('Contact Density Ratio')
ax.set_ylabel('Number of Accounts')
ax.set_title('Contact Density Ratio Distribution')
ax.legend()
ax.set_xlim(0, 100)

# Decision Maker Ratio
ax = axes[0, 1]
dmr_vals = df[df['actual_contacts'] > 0]['decision_maker_ratio']
ax.hist(dmr_vals, bins=30, color='forestgreen', edgecolor='white', alpha=0.7)
ax.axvline(15.0, color='red', linestyle='--', linewidth=2, label='Benchmark (15%)')
ax.set_xlabel('Decision Maker Ratio (%)')
ax.set_ylabel('Number of Accounts')
ax.set_title('Decision Maker Ratio Distribution')
ax.legend()

# Department Coverage
ax = axes[1, 0]
dept_counts = df['dept_coverage'].value_counts().sort_index()
bars = ax.bar(dept_counts.index, dept_counts.values, color='darkorange', edgecolor='white', alpha=0.7)
ax.set_xlabel('Number of Key Departments Covered')
ax.set_ylabel('Number of Accounts')
ax.set_title('Departmental Coverage Distribution (w/ Eng as IT)')
ax.set_xticks(range(0, 6))
for bar, val in zip(bars, dept_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
            f'{val}', ha='center', va='bottom', fontweight='bold')

# Composite Risk
ax = axes[1, 1]
colors_risk = {'Low': 'green', 'Medium': 'yellow', 'High': 'orange', 'Critical': 'red'}
risk_counts = df['risk_category'].value_counts().sort_index()
bars = ax.bar(risk_counts.index, risk_counts.values, 
              color=[colors_risk[c] for c in risk_counts.index], edgecolor='black', alpha=0.7)
ax.set_xlabel('Risk Category')
ax.set_ylabel('Number of Accounts')
ax.set_title('Composite Risk Category Distribution')
for bar, val in zip(bars, risk_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
            f'{val}\n({val/len(df)*100:.1f}%)', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('/work/risk_distribution_v2.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: /work/risk_distribution_v2.png")

# Save updated data
df.to_csv('/work/key_accounts_risk_v2.csv', index=False)
print("\nDone!")