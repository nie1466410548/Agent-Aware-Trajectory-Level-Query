import json, numpy as np, pandas as pd
from scipy import stats

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

df['units_per_eff_hour'] = df['total_units'] / df['total_eff_hours']

top10 = df[df['rank']<=10].sort_values('rank')
print("=== TOP 10 PROFILE ===")
print(top10[['rank','Employee','Gender','Age','Education Level','tenure_months','Team',
             'total_eff_hours','total_units','avg_units','avg_pass_rate','Base Salary','Company Accommodation']].round(2).to_string(index=False))

print("\n=== TOP 10 summary stats ===")
for col in ['Age','tenure_months','total_eff_hours','total_units','avg_units','avg_pass_rate','Base Salary','units_per_eff_hour']:
    print(f"{col}: mean={top10[col].mean():.2f}, min={top10[col].min():.2f}, max={top10[col].max():.2f}")

print("\n=== Correlation avg_units vs avg_pass_rate (overall) ===")
print("r =", round(df['avg_units'].corr(df['avg_pass_rate']),3))

df['units_q'] = pd.qcut(df['avg_units'], 4, labels=['Q1_low','Q2','Q3','Q4_high'])
print("\n=== Avg pass rate by avg_units quartile ===")
print(df.groupby('units_q', observed=True)['avg_pass_rate'].agg(['mean','count']).round(2))

# Disciplinary data - get discipline days per employee via SQL query from earlier S21 archived results
with open('/results/S21.rows.jsonl') as f:
    rows3 = [json.loads(l) for l in f]
dfd = pd.DataFrame(rows3)
dfd.columns = ['Employee ID','Employee','Team','Gender','Age','Education Level','tenure_months','days',
               'total_eff_hours','avg_eff_hours','total_units','avg_units','avg_pass_rate','discipline_days']
df = df.merge(dfd[['Employee ID','discipline_days']], on='Employee ID', how='left')
print("\n=== Disciplinary days: Top 10 vs Rest ===")
top10d = df[df['rank']<=10]
print("Top10 with discipline:", (top10d['discipline_days']>0).sum(), "of", len(top10d))
print("Rest with discipline:", (df[df['rank']>10]['discipline_days']>0).sum(), "of", len(df[df['rank']>10]))

print("\n=== Employees with any discipline record ===")
print(df[df['discipline_days']>0][['Employee','rank','discipline_days']].to_string(index=False))

# Who has highest pass rates combined with high units (potential 'all-rounders')
print("\n=== Top all-rounders by min(percentile of units, percentile of pass, percentile of eff hours) ===")
for col in ['total_eff_hours','total_units','avg_pass_rate']:
    df['pct_'+col] = df[col].rank(pct=True)
df['min_pct'] = df[['pct_total_eff_hours','pct_total_units','pct_avg_pass_rate']].min(axis=1)
print(df.sort_values('min_pct', ascending=False)[['Employee','rank','avg_units','avg_pass_rate','total_eff_hours']].head(10).round(2).to_string(index=False))

# Accommodation association
print("\n=== Company Accommodation ===")
print(pd.crosstab(df['rank']<=10, df['Company Accommodation'], normalize='index').round(3))
print(pd.crosstab(df['rank']<=20, df['Company Accommodation'], normalize='index').round(3))
