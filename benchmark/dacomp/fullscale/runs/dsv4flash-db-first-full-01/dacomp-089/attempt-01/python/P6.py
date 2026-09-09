import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data
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

# ============================================================
# 1. DEVELOP DIFFERENTIATED ASSESSMENT STANDARDS
# ============================================================

# Compute industry-specific benchmarks
print("=" * 60)
print("INDUSTRY-SPECIFIC BENCHMARKS")
print("=" * 60)

industry_benchmarks = df.groupby('industry_normalized').agg({
    'contact_density_ratio': ['mean', 'median', 'std'],
    'decision_maker_ratio': ['mean', 'median'],
    'dept_coverage': ['mean', 'median'],
    'actual_contacts': ['mean', 'median'],
    'number_of_employees': ['mean', 'median']
}).round(2)

print(industry_benchmarks)

# Company size-specific benchmarks
print("\n" + "=" * 60)
print("COMPANY SIZE BENCHMARKS")
print("=" * 60)

size_benchmarks = df.groupby('company_size_category').agg({
    'contact_density_ratio': ['mean', 'median', 'std'],
    'decision_maker_ratio': ['mean', 'median'],
    'dept_coverage': ['mean', 'median'],
    'actual_contacts': ['mean', 'median'],
    'number_of_employees': ['mean', 'median']
}).round(2)

print(size_benchmarks)

# ============================================================
# 2. COMPUTE COMPOSITE RISK SCORE
# ============================================================

# For Contact Density: based on industry-specific percentiles
# For Decision-Maker Ratio: based on whether ≥15% benchmark
# For Department Coverage: based on number of departments covered

# Compute industry-specific percentiles for contact density
industry_cdr_p50 = df.groupby('industry_normalized')['contact_density_ratio'].transform('median')
industry_cdr_p25 = df.groupby('industry_normalized')['contact_density_ratio'].transform(lambda x: x.quantile(0.25))

# Risk score components (0 = no risk, 100 = highest risk)
# 1. Contact Density Risk: based on distance from benchmark 5.0
df['cdr_risk'] = np.where(
    df['contact_density_ratio'].isna(), 100,
    np.where(df['contact_density_ratio'] < 5.0, 
             100 * (1 - df['contact_density_ratio'] / 5.0),  # Below benchmark - proportional risk
             np.where(df['contact_density_ratio'] < 15.0, 50, 0))  # Moderately below
)
df['cdr_risk'] = df['cdr_risk'].clip(0, 100)

# 2. Decision Maker Risk: based on benchmark of 15%
df['dmr_risk'] = np.where(
    df['actual_contacts'] == 0, 100,
    np.where(df['decision_maker_ratio'] < 15.0,
             100 * (1 - df['decision_maker_ratio'] / 15.0),
             0)
)
df['dmr_risk'] = df['dmr_risk'].clip(0, 100)

# 3. Department Coverage Risk: based on coverage of 5 key departments
df['dept_risk'] = 100 * (1 - df['dept_coverage'] / 5.0)

# 4. Customer Health Risk (already existing)
df['health_risk'] = 100 * (1 - df['customer_health_score'] / 100.0)

# Composite risk score (weighted)
df['composite_risk'] = (0.30 * df['cdr_risk'] + 
                         0.25 * df['dmr_risk'] + 
                         0.25 * df['dept_risk'] + 
                         0.20 * df['health_risk'])

# Risk categories
df['risk_category'] = pd.cut(df['composite_risk'], 
                              bins=[0, 30, 50, 70, 100],
                              labels=['Low', 'Medium', 'High', 'Critical'])

print("\n" + "=" * 60)
print("RISK CATEGORY DISTRIBUTION")
print("=" * 60)
print(df['risk_category'].value_counts().sort_index())

print("\nComposite Risk Score Stats:")
print(f"  Mean: {df['composite_risk'].mean():.2f}")
print(f"  Median: {df['composite_risk'].median():.2f}")
print(f"  Std: {df['composite_risk'].std():.2f}")
print(f"  Min: {df['composite_risk'].min():.2f}")
print(f"  Max: {df['composite_risk'].max():.2f}")

# Top 20 highest risk accounts
print("\n" + "=" * 60)
print("TOP 20 HIGHEST RISK ACCOUNTS")
print("=" * 60)
top_risk = df.nlargest(20, 'composite_risk')[
    ['account_name', 'industry_normalized', 'company_size_category', 'annual_revenue',
     'actual_contacts', 'contact_density_ratio', 'decision_maker_ratio', 'dept_coverage',
     'composite_risk', 'risk_category']
]
print(top_risk.to_string(index=False))

# ============================================================
# 3. IDENTIFY HIGH-RISK ACCOUNTS BY SPECIFIC METRIC FAILURES
# ============================================================

print("\n" + "=" * 60)
print("ACCOUNTS FAILING SPECIFIC BENCHMARKS")
print("=" * 60)

# Contact Density fails
cdr_fail = df[df['contact_density_ratio'] < 5.0]
print(f"\nContact Density Ratio < 5.0 (benchmark): {len(cdr_fail)} accounts ({len(cdr_fail)/len(df)*100:.1f}%)")

# Decision Maker fails
dmr_fail = df[(df['actual_contacts'] > 0) & (df['decision_maker_ratio'] < 15.0)]
print(f"Decision Maker Ratio < 15% (benchmark): {len(dmr_fail)} accounts ({len(dmr_fail)/len(df)*100:.1f}%)")

# No contacts at all
no_contacts = df[df['actual_contacts'] == 0]
print(f"No contacts established: {len(no_contacts)} accounts ({len(no_contacts)/len(df)*100:.1f}%)")

# Department coverage fails (less than 3 departments)
dept_fail = df[df['dept_coverage'] < 3]
print(f"Department coverage < 3/5: {len(dept_fail)} accounts ({len(dept_fail)/len(df)*100:.1f}%)")

# All three metrics fail
all_fail = df[(df['contact_density_ratio'] < 5.0) & 
              ((df['actual_contacts'] == 0) | (df['decision_maker_ratio'] < 15.0)) & 
              (df['dept_coverage'] < 3)]
print(f"All three metrics below benchmark: {len(all_fail)} accounts ({len(all_fail)/len(df)*100:.1f}%)")

# ============================================================
# 4. SAVE RESULTS FOR VISUALIZATION
# ============================================================

# Save the full dataframe
df.to_csv('/work/key_accounts_risk_analysis.csv', index=False)
print("\n\nSaved analysis to /work/key_accounts_risk_analysis.csv")