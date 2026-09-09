import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load expense by account from archived result S26
exp_acc = pd.DataFrame(__import__('json').load(open('/results/S26.rows.jsonl')), 
                       columns=['subsidiary_id','accounting_period_ending','account_name','amount'])
exp_acc['dashboard_date'] = pd.to_datetime(exp_acc['accounting_period_ending'])

d = pd.read_csv('/work/metrics_all.csv')
d['dashboard_date'] = pd.to_datetime(d['dashboard_date'])

# Merge expense by account
merged = d.merge(exp_acc, on=['subsidiary_id','dashboard_date'], how='inner')
# Pivot to get each expense type
pivot = merged.pivot_table(index=['subsidiary_id','dashboard_date','is_prehigh','is_healthy','cash_flow_risk_level','first_high_idx','period_idx'],
                           columns='account_name', values='amount', aggfunc='sum').reset_index()

# MoM growth for each expense type
for col in ['Administrative Expense','Marketing Expense','R&D Expense','Travel Expense']:
    pivot[col+'_chg'] = pivot.groupby('subsidiary_id')[col].pct_change()

pre = pivot[pivot['is_prehigh']]
healthy = pivot[pivot['is_healthy']]

print("=== Expense type growth: Pre-High vs Healthy ===")
for col in ['Administrative Expense','Marketing Expense','R&D Expense','Travel Expense']:
    pc = pre[col+'_chg'].mean()
    hc = healthy[col+'_chg'].mean()
    print(f"{col:25s}: pre-high={pc:+.2%}, healthy={hc:+.2%}")

# Expense-to-revenue ratio per category
rev = d[['subsidiary_id','dashboard_date','revenue','is_prehigh','is_healthy']].copy()
for col in ['Administrative Expense','Marketing Expense','R&D Expense','Travel Expense']:
    pivot[col+'_to_rev'] = pivot[col]/pivot['revenue']
    print(f"\n{col}/Revenue: pre-high={pivot.loc[pivot['is_prehigh'], col+'_to_rev'].mean():.3f}, healthy={pivot.loc[pivot['is_healthy'], col+'_to_rev'].mean():.3f}")

# Total expense / revenue in pre-high vs healthy
print(f"\nTotal Expense/Revenue: pre-high={pre['expense'].sum()/pre['revenue'].sum():.3f}, healthy={healthy['expense'].sum()/healthy['revenue'].sum():.3f}")

# ============ FINAL EARLY-WARNING SCORECARD ============
print("\n=========== FINAL EARLY WARNING SCORECARD ===========")
# Build a scoring system: +1 for each of 4 signals
d2 = d.copy()
d2['prev_dso'] = d2.groupby('subsidiary_id')['weighted_average_days_outstanding'].shift(1)
d2['dso_chg'] = d2['weighted_average_days_outstanding'] - d2['prev_dso']
d2['overdue_chg'] = d2['overdue_percentage'] - d2['prev_overdue']

# Signal definitions
sig_dso35 = d2['weighted_average_days_outstanding'] > 35
sig_dsojump = d2['dso_chg'] > 5
sig_revfluc = d2['rev_fluct']
sig_overjump = d2['overdue_chg'] > 1
sig_expgt = d2['exp_chg'] > d2['rev_chg']

d2['score'] = sig_dso35.astype(int) + sig_revfluc.astype(int) + sig_overjump.astype(int) + sig_expgt.astype(int)
d2['score_strict'] = sig_dso35.astype(int) + sig_revfluc.astype(int) + sig_dsojump.astype(int)

pre2 = d2[d2['is_prehigh']]
healthy2 = d2[d2['is_healthy']]

for thresh in [1,2,3,4]:
    sens = (pre2['score']>=thresh).mean()
    spec = 1-(healthy2['score']>=thresh).mean()
    print(f"Score >= {thresh} (DSO>35, RevFluc, OverJump, Exp>Rev): sens={sens:.2%}, spec={spec:.2%}")

for thresh in [1,2,3]:
    sens = (pre2['score_strict']>=thresh).mean()
    spec = 1-(healthy2['score_strict']>=thresh).mean()
    print(f"Strict score >= {thresh} (DSO>35, RevFluc, DSOjump): sens={sens:.2%}, spec={spec:.2%}")

# Distribution of scores in pre-high vs healthy
print("\nScore distribution pre-high:", pre2['score'].value_counts().sort_index().to_dict())
print("Score distribution healthy:", healthy2['score'].value_counts().sort_index().to_dict())

# ============ VIOLIN/BOX PLOT of DSO by context ============
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
# Boxplot DSO by risk context
d3 = d2[['weighted_average_days_outstanding','overdue_percentage','divergence','cash_flow_risk_level']].copy()
d3['risk'] = d3['cash_flow_risk_level']
import seaborn as sns
sns.boxplot(data=d3, x='risk', y='weighted_average_days_outstanding', ax=axes[0], palette='RdYlGn_r')
axes[0].axhline(35, color='orange', linestyle='--', label='DSO=35')
axes[0].axhline(45, color='red', linestyle='--', label='DSO=45')
axes[0].set_title('DSO by Risk Level')
axes[0].legend()

sns.boxplot(data=d3, x='risk', y='overdue_percentage', ax=axes[1], palette='RdYlGn_r')
axes[1].set_title('Overdue % by Risk Level')

# Score by months to high
d2['months_to_high'] = d2['first_high_idx'] - d2['period_idx']
score_mt = d2[(d2['months_to_high']>=0)&(d2['months_to_high']<=7)].groupby('months_to_high')['score'].mean()
axes[2].plot(score_mt.index, score_mt.values, 'o-', color='darkorange')
axes[2].invert_xaxis()
axes[2].set_title('Early-Warning Score by Months-to-High')
axes[2].set_xlabel('Months Before High')
axes[2].set_ylabel('Avg Signal Score (0-4)')
plt.tight_layout()
plt.savefig('/work/risk_levels_boxes.png', dpi=120)
print("Saved risk_levels_boxes.png")

# Per subsidiary pre-high score (last 3 months before High)
print("\n=== Score in final 3 months before High per subsidiary ===")
last3 = d2[(d2['months_to_high']>=0)&(d2['months_to_high']<=3)]
for sub in d2['subsidiary_id'].unique():
    s = last3[last3['subsidiary_id']==sub]
    if len(s):
        print(f"{sub}: avg score last 3mo={s['score'].mean():.2f}, DSO at T-1={s[s['months_to_high']==1]['weighted_average_days_outstanding'].values}, score at T-1={s[s['months_to_high']==1]['score'].values}")
