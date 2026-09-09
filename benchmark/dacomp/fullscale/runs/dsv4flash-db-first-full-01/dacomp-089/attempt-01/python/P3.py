import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# Load the account-level metrics from S40
results_dir = '/results'

accounts = []
with open(f'{results_dir}/S40.rows.jsonl', 'r') as f:
    for line in f:
        accounts.append(json.loads(line))

df_accounts = pd.DataFrame(accounts)
print(f"Total key accounts: {len(df_accounts)}")
print(f"Columns: {df_accounts.columns.tolist()}")

# Basic stats
print(f"\nAccounts with null employees: {df_accounts['number_of_employees'].isna().sum()}")
print(f"Accounts with zero actual_contacts: {(df_accounts['actual_contacts'] == 0).sum()}")
print(f"Accounts with chief_count > 0: {(df_accounts['chief_count'] > 0).sum()}")
print(f"Accounts with decision_maker > 0: {(df_accounts['decision_maker_ratio'] > 0).sum()}")

# Contact density stats
cdr = df_accounts['contact_density_ratio'].dropna()
print(f"\nContact Density Ratio stats:")
print(f"  Mean: {cdr.mean():.2f}")
print(f"  Median: {cdr.median():.2f}")
print(f"  Std: {cdr.std():.2f}")
print(f"  Accounts below benchmark 5.0: {(cdr < 5.0).sum()} / {len(cdr)}")

# Decision maker ratio stats
dmr = df_accounts[df_accounts['actual_contacts'] > 0]['decision_maker_ratio']
print(f"\nDecision Maker Ratio stats (accounts with contacts):")
print(f"  Mean: {dmr.mean():.2f}%")
print(f"  Median: {dmr.median():.2f}%")
print(f"  Accounts with DMR >= 15%: {(dmr >= 15).sum()} / {len(dmr)}")

# Department coverage stats
print(f"\nDepartment Coverage stats:")
print(f"  Mean: {df_accounts['dept_coverage'].mean():.2f}")
print(f"  Median: {df_accounts['dept_coverage'].median():.2f}")
print(f"  Coverage distribution:")
for i in range(6):
    cnt = (df_accounts['dept_coverage'] == i).sum()
    print(f"    {i}/5 departments: {cnt} ({cnt/len(df_accounts)*100:.1f}%)")

# Industry distribution
print(f"\nIndustry distribution (top 10):")
for ind, cnt in df_accounts['industry_normalized'].value_counts().head(10).items():
    print(f"  {ind}: {cnt}")

# Company size category
print(f"\nCompany size category:")
for sz, cnt in df_accounts['company_size_category'].value_counts().items():
    print(f"  {sz}: {cnt}")

# Individual department coverage
print(f"\nIndividual department coverage:")
for dept in ['has_sales', 'has_finance', 'has_operations', 'has_it', 'has_hr']:
    cnt = (df_accounts[dept] == 1).sum()
    print(f"  {dept.replace('has_', '')}: {cnt} ({cnt/len(df_accounts)*100:.1f}%)")