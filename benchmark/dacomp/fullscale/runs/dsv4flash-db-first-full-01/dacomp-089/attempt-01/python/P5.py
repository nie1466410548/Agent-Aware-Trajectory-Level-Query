import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Column names from S40 query
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
print(f"Total key accounts: {len(df)}")
print(f"\nFirst rows:")
print(df.head(3))
print(f"\nData types:")
print(df.dtypes)

# Basic stats
print(f"\nAccounts with null employees: {df['number_of_employees'].isna().sum()}")
print(f"Accounts with zero actual_contacts: {(df['actual_contacts'] == 0).sum()}")
print(f"Accounts with chief_count > 0: {(df['chief_count'] > 0).sum()}")
print(f"Accounts with decision_maker_ratio > 0: {(df['decision_maker_ratio'] > 0).sum()}")

# Contact density stats
cdr = df['contact_density_ratio'].dropna()
print(f"\nContact Density Ratio stats:")
print(f"  Count: {len(cdr)}")
print(f"  Mean: {cdr.mean():.2f}")
print(f"  Median: {cdr.median():.2f}")
print(f"  Std: {cdr.std():.2f}")
print(f"  Accounts below benchmark 5.0: {(cdr < 5.0).sum()} / {len(cdr)} ({(cdr < 5.0).sum()/len(cdr)*100:.1f}%)")

# Decision maker ratio stats
dmr = df[df['actual_contacts'] > 0]['decision_maker_ratio']
print(f"\nDecision Maker Ratio stats (accounts with contacts):")
print(f"  Count: {len(dmr)}")
print(f"  Mean: {dmr.mean():.2f}%")
print(f"  Median: {dmr.median():.2f}%")
print(f"  Accounts with DMR >= 15%: {(dmr >= 15).sum()} / {len(dmr)} ({(dmr >= 15).sum()/len(dmr)*100:.1f}%)")

# Department coverage stats
print(f"\nDepartment Coverage stats:")
print(f"  Mean: {df['dept_coverage'].mean():.2f}")
print(f"  Median: {df['dept_coverage'].median():.2f}")
print(f"  Coverage distribution:")
for i in range(6):
    cnt = (df['dept_coverage'] == i).sum()
    print(f"    {i}/5 departments: {cnt} ({cnt/len(df)*100:.1f}%)")

# Individual department coverage
print(f"\nIndividual department coverage:")
for dept in ['has_sales', 'has_finance', 'has_operations', 'has_it', 'has_hr']:
    cnt = (df[dept] == 1).sum()
    print(f"  {dept.replace('has_', '')}: {cnt} ({cnt/len(df)*100:.1f}%)")

# Industry distribution
print(f"\nIndustry distribution:")
for ind, cnt in df['industry_normalized'].value_counts().items():
    print(f"  {ind}: {cnt}")

# Company size category
print(f"\nCompany size category:")
for sz, cnt in df['company_size_category'].value_counts().items():
    print(f"  {sz}: {cnt}")

# Relationship strength
print(f"\nRelationship strength:")
for rs, cnt in df['relationship_strength'].value_counts().items():
    print(f"  {rs}: {cnt}")

# Churn risk
print(f"\nChurn risk level:")
for cr, cnt in df['churn_risk_level'].value_counts().items():
    print(f"  {cr}: {cnt}")

# Customer health score
print(f"\nCustomer health score stats:")
print(f"  Mean: {df['customer_health_score'].mean():.2f}")
print(f"  Median: {df['customer_health_score'].median():.2f}")
print(f"  Distribution:")
for i in range(0, 101, 10):
    cnt = ((df['customer_health_score'] >= i) & (df['customer_health_score'] < i+10)).sum()
    if cnt > 0:
        print(f"    {i}-{i+9}: {cnt}")