import json
import pandas as pd
import numpy as np
import os

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

# Analysis by company size
print("=" * 70)
print("DIFFERENTIATED STANDARDS BY COMPANY SIZE")
print("=" * 70)
for sz in ['Enterprise', 'Mid-Market']:
    subset = df[df['company_size_category'] == sz]
    print(f"\n--- {sz} (n={len(subset)}) ---")
    print(f"  Employees: mean={subset['number_of_employees'].mean():.0f}, median={subset['number_of_employees'].median():.0f}")
    print(f"  Actual contacts: mean={subset['actual_contacts'].mean():.2f}, median={subset['actual_contacts'].median():.0f}")
    cdr = subset['contact_density_ratio']
    print(f"  CDR percentiles: p10={cdr.quantile(0.10):.2f}, p25={cdr.quantile(0.25):.2f}, p50={cdr.quantile(0.50):.2f}, p75={cdr.quantile(0.75):.2f}, p90={cdr.quantile(0.90):.2f}")
    dmr = subset[subset['actual_contacts'] > 0]['decision_maker_ratio']
    print(f"  DMR percentiles (with contacts): p25={dmr.quantile(0.25):.2f}, p50={dmr.quantile(0.50):.2f}, p75={dmr.quantile(0.75):.2f}, p90={dmr.quantile(0.90):.2f}")
    print(f"  Dept coverage: mean={subset['dept_coverage'].mean():.2f}, median={subset['dept_coverage'].median():.0f}")
    print(f"  Accounts with 0 contacts: {(subset['actual_contacts']==0).sum()} ({(subset['actual_contacts']==0).mean()*100:.1f}%)")
    print(f"  Accounts with 0 dept coverage: {(subset['dept_coverage']==0).sum()} ({(subset['dept_coverage']==0).mean()*100:.1f}%)")

# Analysis by employee count buckets
print("\n" + "=" * 70)
print("ANALYSIS BY EMPLOYEE COUNT BUCKETS")
print("=" * 70)

bins = [0, 50, 100, 200, 500, 1000, 2000, 5000, 100000]
labels = ['<50', '50-100', '100-200', '200-500', '500-1K', '1K-2K', '2K-5K', '5K+']
df['emp_bucket'] = pd.cut(df['number_of_employees'].fillna(0), bins=bins, labels=labels, right=False)

for bucket, subset in df.groupby('emp_bucket', observed=True):
    if len(subset) == 0:
        continue
    cdr = subset['contact_density_ratio']
    dmr = subset[subset['actual_contacts'] > 0]['decision_maker_ratio']
    print(f"\nEmployees {bucket}: n={len(subset)}")
    print(f"  Contacts: mean={subset['actual_contacts'].mean():.1f}, median={subset['actual_contacts'].median():.0f}")
    print(f"  CDR: mean={cdr.mean():.1f}, median={cdr.median():.1f}")
    print(f"  DMR (with contacts): median={dmr.median():.1f}%, mean={dmr.mean():.1f}%")
    print(f"  Coverage: mean={subset['dept_coverage'].mean():.2f}")

# Industry-specific insights - which industries have better/worse profiles
print("\n" + "=" * 70)
print("INDUSTRY PROFILES (CDR pass rate, DMR pass rate, coverage)")
print("=" * 70)
for ind, subset in df.groupby('industry_normalized'):
    cdr_pass = (subset['contact_density_ratio'] >= 5).mean() * 100
    dmr_pass = ((subset['actual_contacts'] == 0) | (subset['decision_maker_ratio'] >= 15)).mean() * 100
    # Actually count accounts with DMR >= 15
    dmr_pass2 = (subset[subset['actual_contacts'] > 0]['decision_maker_ratio'] >= 15).mean() * 100
    zero_contacts = (subset['actual_contacts'] == 0).mean() * 100
    print(f"  {ind}: CDR>=5: {cdr_pass:.0f}% | DMR>=15: {dmr_pass2:.1f}% | 0-contacts: {zero_contacts:.0f}% | coverage: {subset['dept_coverage'].mean():.2f}")

# Contact quality: how many accounts have at least 1 chief contact
print("\nAccounts with at least 1 C-level contact:", (df['chief_count'] > 0).sum())
print("Accounts with 0 contacts:", (df['actual_contacts'] == 0).sum())
print("Accounts with contacts but no C-level:", ((df['actual_contacts'] > 0) & (df['chief_count'] == 0)).sum())