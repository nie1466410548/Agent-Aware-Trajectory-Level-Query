import json, numpy as np, pandas as pd
from scipy import stats

# Reload the ranked dataframe
with open('/results/S27.rows.jsonl') as f:
    rows = [json.loads(l) for l in f]
df = pd.DataFrame(rows)
df.columns = ['Employee ID','Employee','Team','Gender','Age','Education Level','tenure_months','days',
              'total_eff_hours','total_units','avg_units','avg_pass_rate','composite_score','rank']

with open('/results/S29.rows.jsonl') as f:
    rows2 = [json.loads(l) for l in f]
df_sal = pd.DataFrame(rows2)
df_sal.columns = ['Employee ID','Employee','Base Salary','Company Accommodation']
df = df.merge(df_sal, on=['Employee ID','Employee'], how='left')

# Productivity per effective hour
df['units_per_eff_hour'] = df['total_units'] / df['total_eff_hours']

print("=== Units per effective hour by gender ===")
print(df.groupby('Gender')['units_per_eff_hour'].describe().round(2))

# t-test
g = df.groupby('Gender')
fem = df.loc[df.Gender=='Female','units_per_eff_hour']
mal = df.loc[df.Gender=='Male','units_per_eff_hour']
print("\nt-test units/eff_hour female vs male: t=%.3f, p=%.6f" % stats.ttest_ind(fem, mal, equal_var=False))

print("\n=== units/eff_hour by education ===")
print(df.groupby('Education Level')['units_per_eff_hour'].describe().round(2))

# Top 10 detailed profile
print("\n=== TOP 10 PROFILE ===")
top10 = df[df.rank<=10].sort_values('rank')
print(top10[['rank','Employee','Gender','Age','Education Level','tenure_months','Team',
             'total_eff_hours','total_units','avg_units','avg_pass_rate','Base Salary','Company Accommodation']].round(2).to_string(index=False))

print("\n=== TOP 10 summary stats ===")
for col in ['Age','tenure_months','total_eff_hours','total_units','avg_units','avg_pass_rate','Base Salary']:
    print(f"{col}: mean={top10[col].mean():.2f}, min={top10[col].min():.2f}, max={top10[col].max():.2f}")

# Relationship: pass rate vs units tradeoff
print("\n=== Correlation avg_units vs avg_pass_rate (overall) ===")
print("r =", round(df['avg_units'].corr(df['avg_pass_rate']),3))

# Check pass-rate by units quartile - does top producer sacrifice quality?
df['units_q'] = pd.qcut(df['avg_units'], 4, labels=['Q1_low','Q2','Q3','Q4_high'])
print("\n=== Avg pass rate by avg_units quartile ===")
print(df.groupby('units_q', observed=True)['avg_pass_rate'].agg(['mean','count']).round(2))

# Disciplinary issue analysis
# Load discipline from result S21? Let me re-query via Python for discipline
# Actually query it now
