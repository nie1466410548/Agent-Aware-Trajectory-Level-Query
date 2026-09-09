import json
import pandas as pd
import numpy as np
import os

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

# Compute risk scores
df['cdr_risk'] = np.where(df['contact_density_ratio'] < 5.0, 
    100 * (1 - np.minimum(df['contact_density_ratio'] / 5.0, 1.0)),
    np.where(df['contact_density_ratio'] < 15.0, 50, 0)).clip(0, 100)
df['dmr_risk'] = np.where(df['actual_contacts'] == 0, 100,
    np.where(df['decision_maker_ratio'] < 15.0, 100 * (1 - df['decision_maker_ratio'] / 15.0), 0)).clip(0, 100)
df['dept_risk'] = 100 * (1 - df['dept_coverage'] / 5.0)
df['health_risk'] = 100 * (1 - df['customer_health_score'] / 100.0)
df['composite_risk'] = (0.30 * df['cdr_risk'] + 0.25 * df['dmr_risk'] + 
                         0.25 * df['dept_risk'] + 0.20 * df['health_risk'])
df['risk_category'] = pd.cut(df['composite_risk'], bins=[0, 30, 50, 70, 100],
                              labels=['Low', 'Medium', 'High', 'Critical'])

# ============================================================
# PRIORITIZATION AND ACTION PLAN
# ============================================================

# Define action tiers based on risk
# Tier 1 - Critical: Immediate intervention needed
# Tier 2 - High: Short-term remediation needed
# Tier 3 - Medium: Medium-term improvement needed
# Tier 4 - Low: Maintain and monitor

# For each account, determine specific expansion recommendations
def get_recommendations(row):
    recs = []
    
    # Contact density issue
    if row['contact_density_ratio'] < 5.0 or row['actual_contacts'] == 0:
        if row['number_of_employees'] and row['number_of_employees'] > 0:
            target_contacts = max(5, int(np.ceil(row['number_of_employees'] * 5 / 1000)))
            recs.append(f"Add {target_contacts} contacts (current: {row['actual_contacts']}, target density ≥5/1000 employees)")
        else:
            recs.append(f"Establish initial contacts (current: {row['actual_contacts']}, target: at least 5 contacts)")
    
    # Decision-maker gap
    if row['decision_maker_ratio'] < 15.0 and row['actual_contacts'] > 0:
        target_chiefs = max(1, int(np.ceil(row['actual_contacts'] * 0.15)))
        recs.append(f"Add {target_chiefs} C-level/V-level contacts (current: {row['chief_count']}, target: ≥{target_chiefs})")
    elif row['actual_contacts'] == 0:
        recs.append("Prioritize C-level contact acquisition (CEO, CFO, CTO, etc.)")
    
    # Department coverage gaps
    missing_depts = []
    if row['has_sales'] == 0:
        missing_depts.append('Sales')
    if row['has_finance'] == 0:
        missing_depts.append('Finance')
    if row['has_operations'] == 0:
        missing_depts.append('Operations')
    if row['has_it'] == 0:
        missing_depts.append('IT')
    if row['has_hr'] == 0:
        missing_depts.append('HR')
    
    if missing_depts:
        recs.append(f"Expand coverage to departments: {', '.join(missing_depts)}")
    
    # Health score issue
    if row['customer_health_score'] < 30:
        recs.append("Critical health score - conduct account review immediately")
    elif row['customer_health_score'] < 50:
        recs.append("Below-average health score - schedule strategic check-in")
    
    return '; '.join(recs) if recs else 'Maintain current contact strategy'

df['recommendations'] = df.apply(get_recommendations, axis=1)

# Priority ranking
df['priority_score'] = df['composite_risk'] * 0.7 + (100 - df['customer_health_score']) * 0.3
df['priority_tier'] = pd.cut(df['priority_score'], 
                              bins=[0, 30, 50, 70, 100],
                              labels=['Tier 4: Monitor', 'Tier 3: Improve', 'Tier 2: Short-term', 'Tier 1: Immediate'])

print("Priority Tier Distribution:")
print(df['priority_tier'].value_counts().sort_index())

# Top 20 accounts with recommendations
print("\n" + "=" * 100)
print("TOP 20 PRIORITY ACCOUNTS WITH ACTION RECOMMENDATIONS")
print("=" * 100)
top_priority = df.nlargest(20, 'priority_score')[
    ['account_name', 'industry_normalized', 'annual_revenue', 'composite_risk', 
     'risk_category', 'priority_tier', 'recommendations']
]
for i, (_, row) in enumerate(top_priority.iterrows()):
    print(f"\n{i+1}. {row['account_name']} ({row['industry_normalized']}) - ${row['annual_revenue']:,.0f}")
    print(f"   Risk: {row['composite_risk']:.0f} - {row['risk_category']} | {row['priority_tier']}")
    print(f"   Action: {row['recommendations']}")

# ============================================================
# INDUSTRY-SPECIFIC ACTION PLANS
# ============================================================
print("\n" + "=" * 100)
print("INDUSTRY-SPECIFIC OPTIMIZATION PLANS")
print("=" * 100)

industry_risk = df.groupby('industry_normalized').agg({
    'composite_risk': 'mean',
    'contact_density_ratio': 'mean',
    'decision_maker_ratio': 'mean',
    'dept_coverage': 'mean',
    'customer_health_score': 'mean',
    'actual_contacts': 'mean',
    'number_of_employees': 'mean',
    'account_id': 'count'
}).round(2)
industry_risk.columns = ['avg_risk', 'avg_cdr', 'avg_dmr', 'avg_dept', 'avg_health', 
                          'avg_contacts', 'avg_employees', 'account_count']
industry_risk = industry_risk.sort_values('avg_risk', ascending=False)

for ind, row in industry_risk.iterrows():
    print(f"\n{ind} ({int(row['account_count'])} accounts):")
    print(f"   Avg Risk: {row['avg_risk']:.1f} | CDR: {row['avg_cdr']:.1f} | DMR: {row['avg_dmr']:.1f}% | Coverage: {row['avg_dept']:.1f}/5")
    
    # Specific recommendations by industry
    if row['avg_cdr'] < 5:
        print(f"   >> CRITICAL: Very low contact density. Need to increase contacts by {max(5, int(row['avg_employees'] * 5 / 1000))}x on average.")
    if row['avg_dmr'] < 15:
        print(f"   >> Decision-maker acquisition needed.")
    if row['avg_dept'] < 2:
        print(f"   >> Departmental coverage severely lacking. Focus on multi-department outreach.")

# Save prioritized action plan
df.to_csv('/work/action_plan.csv', index=False)
print("\n\nSaved action plan to /work/action_plan.csv")

# Summary statistics
print("\n" + "=" * 60)
print("EXECUTIVE SUMMARY")
print("=" * 60)
print(f"Total Key Accounts (Top 20% by Revenue): {len(df)}")
print(f"  - Revenue range: ${df['annual_revenue'].min():,.0f} - ${df['annual_revenue'].max():,.0f}")
print(f"  - Avg revenue: ${df['annual_revenue'].mean():,.0f}")
print(f"\nRisk Distribution:")
for cat in ['Critical', 'High', 'Medium', 'Low']:
    cnt = (df['risk_category'] == cat).sum()
    print(f"  {cat}: {cnt} ({cnt/len(df)*100:.1f}%)")
print(f"\nPriority Tier Distribution:")
for tier in ['Tier 1: Immediate', 'Tier 2: Short-term', 'Tier 3: Improve', 'Tier 4: Monitor']:
    cnt = (df['priority_tier'] == tier).sum()
    print(f"  {tier}: {cnt} ({cnt/len(df)*100:.1f}%)")