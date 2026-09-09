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
df['employees_known'] = df['number_of_employees'].notna() & (df['number_of_employees'] > 0)

# ============================================================
# DIFFERENTIATED ASSESSMENT STANDARDS
# ============================================================
# Based on customer size (company_size_category / employees):
# - Mid-Market (< 1000 employees): standard CDR >= 5.0 (task benchmark achievable)
# - Enterprise (>= 1000 employees): adjusted standard CDR >= 1.0 
#   (because 5/1000 would require 25+ contacts for 5000-employee firms; 
#    the data shows median 0.5, p75 0.84, so 1.0 is aspirational but attainable)

# Determine size segment by employees where available, fallback to company_size_category
df['size_segment'] = np.where(
    df['employees_known'] & (df['number_of_employees'] >= 1000), 'Enterprise',
    np.where(df['employees_known'], 'Mid-Market', df['company_size_category'].fillna('Mid-Market'))
)
df['size_segment'] = np.where(df['size_segment'] == 'Enterprise', 'Enterprise', 'Mid-Market')

# CDR standards by size
df['cdr_benchmark'] = np.where(df['size_segment'] == 'Enterprise', 1.0, 5.0)
df['cdr_amber'] = np.where(df['size_segment'] == 'Enterprise', 0.5, 2.5)

# CDR Risk score (0=pass, 50=amber zone, 100=red)
def cdr_score(row):
    if row['actual_contacts'] == 0:
        return 100
    if row['contact_density_ratio'] >= row['cdr_benchmark']:
        return 0
    if row['contact_density_ratio'] >= row['cdr_amber']:
        return 50
    # Red: below amber
    return min(100, 50 + 50 * (1 - row['contact_density_ratio'] / row['cdr_amber']))

df['cdr_risk'] = df.apply(cdr_score, axis=1)

# DMR standard (universal 15%): 
# accounts with no contacts = 100 risk; DMR >= 15 = 0; below = proportional
def dmr_score(row):
    if row['actual_contacts'] == 0:
        return 100
    if row['decision_maker_ratio'] >= 15:
        return 0
    if row['decision_maker_ratio'] >= 5:
        return 50
    return min(100, 50 + 50 * (1 - row['decision_maker_ratio'] / 5.0))

df['dmr_risk'] = df.apply(dmr_score, axis=1)

# Department coverage standard: 5 key departments
# 0-1 dept = red, 2 dept = amber, 3+ dept = acceptable, 5 = full
def dept_score(row):
    c = row['dept_coverage']
    if c >= 3:
        return 0
    if c == 2:
        return 50
    if c == 1:
        return 75
    return 100

df['dept_risk'] = df.apply(dept_score, axis=1)

# Health score risk (0-100)
df['health_risk'] = 100 * (1 - df['customer_health_score'] / 100.0)

# Composite risk score - weighted
df['composite_risk'] = (0.30 * df['cdr_risk'] + 
                         0.25 * df['dmr_risk'] + 
                         0.25 * df['dept_risk'] + 
                         0.20 * df['health_risk']).round(1)

df['risk_category'] = pd.cut(df['composite_risk'], 
                              bins=[0, 25, 45, 65, 100],
                              labels=['Low Risk', 'Medium Risk', 'High Risk', 'Critical'])

print("Final Differentiated Risk Distribution:")
print(df['risk_category'].value_counts().sort_index())
print(f"\nComposite Risk Stats:")
print(f"  Mean: {df['composite_risk'].mean():.2f}")
print(f"  Median: {df['composite_risk'].median():.2f}")

# Priority tiers based on risk + health
df['priority_score'] = df['composite_risk'] * 0.7 + df['health_risk'] * 0.3
df['priority_tier'] = np.where(df['priority_score'] >= 75, 'Tier 1: Immediate Action',
                     np.where(df['priority_score'] >= 55, 'Tier 2: Short-Term (30-60 days)',
                     np.where(df['priority_score'] >= 40, 'Tier 3: Medium-Term (60-90 days)',
                              'Tier 4: Monitor & Maintain')))

print("\nPriority Tier Distribution:")
print(df['priority_tier'].value_counts().sort_index())

# ============================================================
# GENERATE SPECIFIC RECOMMENDATIONS
# ============================================================
def get_recommendations(row):
    recs = []
    # CDR
    if row['actual_contacts'] == 0:
        n_target = 5 if row['size_segment'] == 'Mid-Market' else max(10, int(np.ceil(row['number_of_employees'] * 1.0 / 1000))) if row['employees_known'] else 10
        recs.append(f"Establish baseline contact set: acquire {n_target} contacts")
    elif row['contact_density_ratio'] < row['cdr_benchmark']:
        n_target = max(5, int(np.ceil(row['number_of_employees'] * row['cdr_benchmark'] / 1000))) if row['employees_known'] else 5
        recs.append(f"Expand contacts to reach CDR >= {row['cdr_benchmark']:.1f}: add {max(0, n_target - row['actual_contacts'])} more contacts (target ~{n_target})")
    # DMR
    if row['actual_contacts'] == 0:
        recs.append("Acquire C-level contacts first (CEO/CFO/CTO/COO)")
    elif row['chief_count'] == 0:
        recs.append("Add at least 1 C-level/executive decision-maker contact")
    elif row['decision_maker_ratio'] < 15:
        n_chiefs = int(np.ceil(row['actual_contacts'] * 0.15)) - row['chief_count']
        recs.append(f"Add {max(1, n_chiefs)} more C-level contacts to reach >= 15% DMR")
    # Coverage
    missing = []
    if row['has_sales'] == 0: missing.append('Sales')
    if row['has_finance'] == 0: missing.append('Finance')
    if row['has_operations'] == 0: missing.append('Operations')
    if row['has_it'] == 0: missing.append('IT/Engineering')
    if row['has_hr'] == 0: missing.append('HR')
    if missing:
        recs.append(f"Fill department gaps: {', '.join(missing)}")
    if row['customer_health_score'] < 40:
        recs.append("Conduct strategic account review (health score < 40)")
    return ' | '.join(recs)

df['recommendations'] = df.apply(get_recommendations, axis=1)

# Save final
df.to_csv('/work/final_risk_analysis.csv', index=False)

# ============================================================
# Summary for report
# ============================================================
print("\n" + "=" * 80)
print("KEY METRICS SUMMARY - TOP 20% KEY ACCOUNTS")
print("=" * 80)
print(f"Total key accounts: {len(df)}")
print(f"Avg revenue: ${df['annual_revenue'].mean():,.0f}")
print(f"\n1. CONTACT DENSITY RATIO (benchmark >=5 mid-market / >=1.0 enterprise):")
print(f"   Accounts passing: {((df['contact_density_ratio'] >= df['cdr_benchmark'])).sum()} ({(df['contact_density_ratio'] >= df['cdr_benchmark']).mean()*100:.1f}%)")
print(f"   Zero-contact accounts: {(df['actual_contacts']==0).sum()} ({(df['actual_contacts']==0).mean()*100:.1f}%)")

print(f"\n2. DECISION-MAKER RATIO (benchmark >=15%):")
print(f"   Accounts with DMR >= 15%: {(df['decision_maker_ratio']>=15).sum()} ({(df['decision_maker_ratio']>=15).mean()*100:.1f}%)")
print(f"   Accounts with any C-level: {(df['chief_count']>0).sum()}")

print(f"\n3. DEPARTMENTAL COVERAGE (5 departments: Sales, Finance, Operations, IT, HR):")
print(f"   Accounts with 3+ departments: {(df['dept_coverage']>=3).sum()} ({(df['dept_coverage']>=3).mean()*100:.1f}%)")
print(f"   Accounts with 0 departments: {(df['dept_coverage']==0).sum()} ({(df['dept_coverage']==0).mean()*100:.1f}%)")
print(f"   Avg coverage: {df['dept_coverage'].mean():.2f}/5")

# Which accounts need which actions - volume estimates
print(f"\n4. ACTION VOLUMES:")
print(f"   Need new contacts (0 contacts): {(df['actual_contacts']==0).sum()}")
print(f"   Need C-level contacts: {((df['chief_count']==0)).sum()}")
print(f"   Need dept expansion (2 or fewer depts): {(df['dept_coverage']<=2).sum()}")

# Show top 15 by priority for the report
print("\n" + "=" * 80)
print("TOP 15 PRIORITY ACCOUNTS FOR IMMEDIATE ACTION")
print("=" * 80)
top15 = df.nlargest(15, 'priority_score')[['account_name', 'industry_normalized', 'size_segment', 
                                            'annual_revenue', 'actual_contacts', 'chief_count', 
                                            'contact_density_ratio', 'decision_maker_ratio', 
                                            'dept_coverage', 'composite_risk', 'risk_category', 'priority_tier']]
for i, (_, r) in enumerate(top15.iterrows()):
    print(f"{i+1}. {r['account_name']} | {r['industry_normalized']} | {r['size_segment']} | ${r['annual_revenue']:,.0f}")
    print(f"   Contacts: {r['actual_contacts']} | C-level: {r['chief_count']} | CDR: {r['contact_density_ratio']:.1f} | DMR: {r['decision_maker_ratio']:.0f}% | Coverage: {r['dept_coverage']}/5")
    print(f"   Risk: {r['composite_risk']:.1f} ({r['risk_category']}) | {r['priority_tier']}")
    print(f"   Rec: {df.loc[df['account_id']==r['account_id'], 'recommendations'].values[0]}")
    print()