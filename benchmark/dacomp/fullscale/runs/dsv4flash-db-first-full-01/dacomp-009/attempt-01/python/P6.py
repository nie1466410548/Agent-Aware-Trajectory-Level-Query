import json, numpy as np, pandas as pd

with open('/results/S27.rows.jsonl') as f:
    rows = [json.loads(l) for l in f]
df = pd.DataFrame(rows)
df.columns = ['Employee ID','Employee','Team','Gender','Age','Education Level','tenure_months','days',
              'total_eff_hours','total_units','avg_units','avg_pass_rate','composite_score','rank']

with open('/results/S21.rows.jsonl') as f:
    rows3 = [json.loads(l) for l in f]
dfd = pd.DataFrame(rows3)
dfd.columns = ['Employee ID','Employee','Team','Gender','Age','Education Level','tenure_months','days',
               'total_eff_hours','avg_eff_hours','total_units','avg_units','avg_pass_rate','discipline_days']
df = df.merge(dfd[['Employee ID','avg_eff_hours']], on='Employee ID', how='left')

def compute_score(df, w_eh, w_u, w_p, use_avg=False):
    if use_avg:
        a, b, c = df['avg_eff_hours'].values, df['avg_units'].values, df['avg_pass_rate'].values
    else:
        a, b, c = df['total_eff_hours'].values, df['total_units'].values, df['avg_pass_rate'].values
    na = (a - a.min())/(a.max()-a.min())
    nb = (b - b.min())/(b.max()-b.min())
    nc = (c - c.min())/(c.max()-c.min())
    score = w_eh*na + w_u*nb + w_p*nc
    return pd.Series(score, index=df.index).rank(ascending=False).astype(int)

scenarios = [
    ('Equal (1/3,1/3,1/3)', 1/3, 1/3, 1/3, False),
    ('Quality-focused (0.2,0.3,0.5)', 0.2, 0.3, 0.5, False),
    ('Output-focused (0.2,0.6,0.2)', 0.2, 0.6, 0.2, False),
    ('Time-focused (0.5,0.3,0.2)', 0.5, 0.3, 0.2, False),
    ('Equal, per-day avg', 1/3, 1/3, 1/3, True),
]
print("=== Top 10 under each scheme ===")
top_sets = {}
for name, w1, w2, w3, use_avg in scenarios:
    r = compute_score(df, w1, w2, w3, use_avg)
    top_ids = set(df.loc[r<=10, 'Employee'])
    top_sets[name] = top_ids
    print(f"{name:32s}: {sorted(top_ids)}")

base = top_sets['Equal (1/3,1/3,1/3)']
for name, s in top_sets.items():
    jac = len(s & base)/len(s | base)
    print(f"Jaccard with baseline Top10: {name:32s} -> {jac:.2f}")

print("\n=== Composite by Gender x Team ===")
print(df.groupby(['Team','Gender'])['composite_score'].agg(['mean','count']).round(3))

print("\n=== Composite by Gender x Education ===")
print(df.groupby(['Education Level','Gender'])['composite_score'].agg(['mean','count']).round(3))

print("\n=== Age distribution top10 ===")
print(df[df['rank']<=10]['Age'].value_counts().sort_index())

# How many of the top 10 are common to all 5 scenarios?
common = set.intersection(*top_sets.values())
print("\nEmployees in Top 10 under ALL 5 scenarios:", sorted(common))

# Male best performers profile
print("\n=== Top male employees ===")
males = df[df['Gender']=='Male'].sort_values('rank').head(5)
print(males[['rank','Employee','Age','Education Level','tenure_months','avg_units','avg_pass_rate','total_eff_hours']].round(2).to_string(index=False))

# Correlation of effective hours and away metrics with units
with open('/results/S32.rows.jsonl') as f:
    pass
