import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load data from result file
rows = []
with open('/results/S36.rows.jsonl', 'r') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows)
print(f"Total records: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print(df[['salary_min', 'salary_max']].describe())

# Compute midpoint salary
df['salary_mid'] = (df['salary_min'] + df['salary_max']) / 2.0
print(f"\nSalary midpoint stats:")
print(df['salary_mid'].describe())

# Filter out extreme outliers
df_clean = df[(df['salary_min'] >= 1000) & (df['salary_max'] <= 50000) & (df['salary_mid'] >= 1000)]
print(f"\nAfter filtering outliers: {len(df_clean)} records")

# Salary distribution - histogram
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df_clean['salary_mid'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_xlabel('Monthly Salary Midpoint (yuan)', fontsize=12)
axes[0].set_ylabel('Number of Job Postings', fontsize=12)
axes[0].set_title('Distribution of Starting Salaries\nfor Vocational School Graduates', fontsize=13)
axes[0].axvline(df_clean['salary_mid'].mean(), color='red', linestyle='--', label=f'Mean: {df_clean["salary_mid"].mean():.0f}')
axes[0].axvline(df_clean['salary_mid'].median(), color='green', linestyle='--', label=f'Median: {df_clean["salary_mid"].median():.0f}')
axes[0].legend()

axes[1].boxplot([df_clean['salary_min'], df_clean['salary_max']], labels=['Salary Min', 'Salary Max'])
axes[1].set_ylabel('Monthly Salary (yuan)', fontsize=12)
axes[1].set_title('Salary Range Distribution', fontsize=13)

plt.tight_layout()
plt.savefig('/work/salary_distribution.png', dpi=150)
plt.close()
print("Saved salary_distribution.png")