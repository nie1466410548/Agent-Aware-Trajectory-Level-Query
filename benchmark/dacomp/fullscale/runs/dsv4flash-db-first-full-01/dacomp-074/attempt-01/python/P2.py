import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

d = pd.read_csv('/work/metrics_all.csv')
d['dashboard_date'] = pd.to_datetime(d['dashboard_date'])

# ============== DIMENSION 1: Revenue Fluctuation ==============
# Frequency of monthly revenue fluctuations exceeding 20%
rev_fluct = d.groupby('is_prehigh').agg(
    total_months=('rev_fluct','count'),
    fluct_months=('rev_fluct','sum'),
    fluct_rate=('rev_fluct','mean')
).reset_index()
rev_fluct['context'] = rev_fluct['is_prehigh'].map({True:'Pre-High (6mo window)', False:'Other periods'})
print("=== Revenue Fluctuation (>20% MoM) ===")
print(rev_fluct[['context','total_months','fluct_months','fluct_rate']])

# Also by subsidiary
sub_rev = d.groupby(['subsidiary_id','is_prehigh']).agg(
    total=('rev_fluct','count'),
    fluct=('rev_fluct','sum')
).reset_index()
sub_rev['rate'] = sub_rev['fluct']/sub_rev['total']
print("\n--- Per subsidiary ---")
print(sub_rev.pivot_table(index='subsidiary_id', columns='is_prehigh', values='rate', aggfunc='first'))

# ============== DIMENSION 2: AR Management ==============
# Proportion of time weighted_average_days_outstanding > 45 days
dso_gt45 = d.groupby('is_prehigh')['dso_gt45'].agg(['count','sum','mean']).reset_index()
dso_gt45['context'] = dso_gt45['is_prehigh'].map({True:'Pre-High (6mo window)', False:'Other periods'})
print("\n=== Days Outstanding > 45 days ===")
print(dso_gt45[['context','count','sum','mean']])

# Instances of 3 consecutive months of overdue_percentage rising
overdue_rise3 = d.groupby('is_prehigh')['overdue_rise3'].agg(['count','sum','mean']).reset_index()
overdue_rise3['context'] = overdue_rise3['is_prehigh'].map({True:'Pre-High (6mo window)', False:'Other periods'})
print("\n=== 3 Consecutive Months Overdue Rising ===")
print(overdue_rise3[['context','count','sum','mean']])

# ============== DIMENSION 3: Expense Control ==============
# Divergence between expense growth rate and revenue growth rate
diverg = d.groupby('is_prehigh')['divergence'].agg(['mean','std','count']).reset_index()
diverg['context'] = diverg['is_prehigh'].map({True:'Pre-High (6mo window)', False:'Other periods'})
print("\n=== Expense-Revenue Growth Divergence (exp_chg - rev_chg pp) ===")
print(diverg[['context','count','mean','std']])

# Also compare pre-high vs healthy specifically
print("\n=== Pre-High vs Healthy (Low) Periods ===")
comp = d[d['is_prehigh'] | d['is_healthy']].copy()
comp['group'] = comp['is_prehigh'].map({True:'Pre-High (6mo)', False:'Healthy (Low risk)'})

# Revenue fluctuation
print("\nRevenue fluctuation rate:")
print(comp.groupby('group')['rev_fluct'].mean())

# DSO > 45
print("\nDSO > 45 rate:")
print(comp.groupby('group')['dso_gt45'].mean())

# 3-month overdue rise
print("\n3-month overdue rise rate:")
print(comp.groupby('group')['overdue_rise3'].mean())

# Expense-revenue divergence
print("\nExpense-revenue divergence (mean):")
print(comp.groupby('group')['divergence'].mean())

# Average overdue_percentage
print("\nAvg overdue_percentage:")
print(comp.groupby('group')['overdue_percentage'].mean())

# Average DSO
print("\nAvg days outstanding:")
print(comp.groupby('group')['weighted_average_days_outstanding'].mean())

# Cross-tab: pre-High flags
print("\n=== Cross-tab flag rates in pre-High ===")
pre = d[d['is_prehigh']]
print("Rev fluct >20%:", pre['rev_fluct'].mean())
print("DSO >45:", pre['dso_gt45'].mean())
print("3mo overdue rise:", pre['overdue_rise3'].mean())
print("Mean divergence:", pre['divergence'].mean())
print("Std divergence:", pre['divergence'].std())

healthy = d[d['is_healthy']]
print("\n=== Cross-tab flag rates in Healthy ===")
print("Rev fluct >20%:", healthy['rev_fluct'].mean())
print("DSO >45:", healthy['dso_gt45'].mean())
print("3mo overdue rise:", healthy['overdue_rise3'].mean())
print("Mean divergence:", healthy['divergence'].mean())
print("Std divergence:", healthy['divergence'].std())

# ============== FIGURES ==============
fig, axes = plt.subplots(2,2, figsize=(14,10))

# 1. Revenue fluctuation rate comparison
groups = ['Pre-High\n(6mo window)', 'Healthy\n(Low risk)']
rates = [pre['rev_fluct'].mean(), healthy['rev_fluct'].mean()]
axes[0,0].bar(groups, rates, color=['crimson','forestgreen'], alpha=0.7)
axes[0,0].set_ylabel('Rate of months with >20% fluctuation')
axes[0,0].set_title('Revenue Fluctuation Frequency')
for i,v in enumerate(rates): axes[0,0].text(i, v+0.01, f'{v:.2%}', ha='center')

# 2. DSO >45 rate
rates2 = [pre['dso_gt45'].mean(), healthy['dso_gt45'].mean()]
axes[0,1].bar(groups, rates2, color=['crimson','forestgreen'], alpha=0.7)
axes[0,1].set_ylabel('Proportion of months')
axes[0,1].set_title('Weighted Avg Days Outstanding > 45 days')
for i,v in enumerate(rates2): axes[0,1].text(i, v+0.01, f'{v:.2%}', ha='center')

# 3. 3-month overdue rise rate
rates3 = [pre['overdue_rise3'].mean(), healthy['overdue_rise3'].mean()]
axes[1,0].bar(groups, rates3, color=['crimson','forestgreen'], alpha=0.7)
axes[1,0].set_ylabel('Rate of 3-consecutive-month rises')
axes[1,0].set_title('Overdue Percentage Consecutive Rise')
for i,v in enumerate(rates3): axes[1,0].text(i, v+0.01, f'{v:.2%}', ha='center')

# 4. Expense-revenue divergence
rates4 = [pre['divergence'].mean(), healthy['divergence'].mean()]
axes[1,1].bar(groups, rates4, color=['crimson','forestgreen'], alpha=0.7)
axes[1,1].set_ylabel('Expense growth - Revenue growth (pp)')
axes[1,1].set_title('Expense-Revenue Growth Divergence')
for i,v in enumerate(rates4): 
    axes[1,1].text(i, v+0.003 if v>=0 else v-0.01, f'{v:.2%}', ha='center')

plt.tight_layout()
plt.savefig('/work/comparison_metrics.png', dpi=120)
print("\nSaved comparison_metrics.png")

# ============== TIME SERIES ==============
# Plot trajectories for pre-high subsidiaries
fig2, axes2 = plt.subplots(2,2, figsize=(14,10))

# Average revenue by period
subs_pre = d[d['subsidiary_id'].isin(d[d['is_prehigh']]['subsidiary_id'].unique())]
pivot_rev = subs_pre.pivot_table(index='period_idx', columns='is_prehigh', values='revenue', aggfunc='mean')
pivot_rev.plot(ax=axes2[0,0], marker='o')
axes2[0,0].set_title('Average Revenue by Period Index')
axes2[0,0].set_xlabel('Period Index')
axes2[0,0].set_ylabel('Revenue')

# Average expense
pivot_exp = subs_pre.pivot_table(index='period_idx', columns='is_prehigh', values='expense', aggfunc='mean')
pivot_exp.plot(ax=axes2[0,1], marker='o', color=['crimson','forestgreen'])
axes2[0,1].set_title('Average Expense by Period Index')
axes2[0,1].set_xlabel('Period Index')
axes2[0,1].set_ylabel('Expense')

# DSO by period
pivot_dso = subs_pre.pivot_table(index='period_idx', columns='is_prehigh', values='weighted_average_days_outstanding', aggfunc='mean')
pivot_dso.plot(ax=axes2[1,0], marker='o', color=['crimson','forestgreen'])
axes2[1,0].axhline(y=45, color='grey', linestyle='--', alpha=0.5)
axes2[1,0].set_title('Avg Days Outstanding by Period Index')
axes2[1,0].set_xlabel('Period Index')
axes2[1,0].set_ylabel('Days Outstanding')

# Overdue percentage by period
pivot_od = subs_pre.pivot_table(index='period_idx', columns='is_prehigh', values='overdue_percentage', aggfunc='mean')
pivot_od.plot(ax=axes2[1,1], marker='o', color=['crimson','forestgreen'])
axes2[1,1].set_title('Avg Overdue % by Period Index')
axes2[1,1].set_xlabel('Period Index')
axes2[1,1].set_ylabel('Overdue %')

plt.tight_layout()
plt.savefig('/work/trajectories.png', dpi=120)
print("Saved trajectories.png")

# ============== KEY INDICATOR THRESHOLD ANALYSIS ==============
# What thresholds can provide 2-3 month early warning?
# Look at pre-High period indices and see when indicators diverge
print("\n=== Early Warning Signal Analysis ===")
# For each subsidiary, compute the cumulative flag count in the pre-High window
pre_detail = d[d['is_prehigh']].copy()
pre_detail['months_to_high'] = pre_detail['first_high_idx'] - pre_detail['period_idx']
print("\nAverage metrics by months-until-high:")
timeline = pre_detail.groupby('months_to_high').agg(
    rev_fluct=('rev_fluct','mean'),
    dso_gt45=('dso_gt45','mean'),
    overdue_rise3=('overdue_rise3','mean'),
    divergence=('divergence','mean'),
    avg_dso=('weighted_average_days_outstanding','mean'),
    avg_overdue=('overdue_percentage','mean')
).reset_index()
print(timeline.sort_values('months_to_high', ascending=False).to_string())

# Specific threshold investigation
print("\n=== Threshold Candidate Analysis ===")
# DSO threshold: 45 days
print(f"DSO > 45 sensitivity in pre-high: {pre['dso_gt45'].mean():.2%}")
print(f"DSO > 45 specificity (healthy): {1-healthy['dso_gt45'].mean():.2%}")

# Revenue fluctuation threshold
print(f"Rev fluct >20% sensitivity: {pre['rev_fluct'].mean():.2%}")
print(f"Rev fluct >20% healthy rate: {healthy['rev_fluct'].mean():.2%}")

# Combined: DSO > 45 AND rev fluct >20%
pre['combo1'] = pre['dso_gt45'] & pre['rev_fluct']
healthy['combo1'] = healthy['dso_gt45'] & healthy['rev_fluct']
print(f"Combo (DSO>45 & RevFluc>20%) sensitivity: {pre['combo1'].mean():.2%}")
print(f"Combo (DSO>45 & RevFluc>20%) healthy rate: {healthy['combo1'].mean():.2%}")

# Try DSO > 50
pre['dso_gt50'] = pre['weighted_average_days_outstanding'] > 50
healthy['dso_gt50'] = healthy['weighted_average_days_outstanding'] > 50
print(f"\nDSO > 50 sensitivity: {pre['dso_gt50'].mean():.2%}")
print(f"DSO > 50 healthy rate: {healthy['dso_gt50'].mean():.2%}")

# Try overdue_percentage > 10%
pre['overdue_gt10'] = pre['overdue_percentage'] > 10
healthy['overdue_gt10'] = healthy['overdue_percentage'] > 10
print(f"\nOverdue > 10% sensitivity: {pre['overdue_gt10'].mean():.2%}")
print(f"Overdue > 10% healthy rate: {healthy['overdue_gt10'].mean():.2%}")

# Try divergence > 0.30 (expense growing 30pp faster than revenue)
pre['div_gt30'] = pre['divergence'] > 0.30
healthy['div_gt30'] = healthy['divergence'] > 0.30
print(f"\nDivergence > 30pp sensitivity: {pre['div_gt30'].mean():.2%}")
print(f"Divergence > 30pp healthy rate: {healthy['div_gt30'].mean():.2%}")

# Best combo: look at any 2 out of 3 flags
pre['any2'] = (pre['dso_gt45'].astype(int) + pre['rev_fluct'].astype(int) + pre['overdue_rise3'].astype(int)) >= 2
healthy['any2'] = (healthy['dso_gt45'].astype(int) + healthy['rev_fluct'].astype(int) + healthy['overdue_rise3'].astype(int)) >= 2
print(f"\nAny 2 of 3 flags sensitivity: {pre['any2'].mean():.2%}")
print(f"Any 2 of 3 flags healthy rate: {healthy['any2'].mean():.2%}")

# Check at 2-3 months before High
pre_early = pre[pre['months_to_high'] >= 3]  # 3+ months before
pre_late = pre[pre['months_to_high'] <= 2]   # 0-2 months before
print(f"\n=== Early (3-6mo before) vs Late (0-2mo before) ===")
print(f"Early (>=3mo): DSO>45={pre_early['dso_gt45'].mean():.2%}, RevFluc={pre_early['rev_fluct'].mean():.2%}, 3moRise={pre_early['overdue_rise3'].mean():.2%}")
print(f"Late (<=2mo):  DSO>45={pre_late['dso_gt45'].mean():.2%}, RevFluc={pre_late['rev_fluct'].mean():.2%}, 3moRise={pre_late['overdue_rise3'].mean():.2%}")

# Early warning signal: DSO > 45 OR revenue drop > 20%
pre['early_warn'] = pre['dso_gt45'] | pre['rev_fluct']
healthy['early_warn'] = healthy['dso_gt45'] | healthy['rev_fluct']
print(f"\nEarly Warning (DSO>45 OR RevFluc>20%) sensitivity: {pre['early_warn'].mean():.2%}")
print(f"Early Warning (DSO>45 OR RevFluc>20%) healthy rate: {healthy['early_warn'].mean():.2%}")

# Multi-month sustained signal
print("\n=== Multi-month Sustained Analysis ===")
# Count consecutive months where each flag is true
def count_consecutive(series):
    cnt = 0
    maxc = 0
    for v in series:
        if v:
            cnt += 1
            maxc = max(maxc, cnt)
        else:
            cnt = 0
    return maxc

for sub in d['subsidiary_id'].unique():
    sub_pre = d[(d['subsidiary_id']==sub) & d['is_prehigh']].sort_values('period_idx')
    if len(sub_pre) > 0:
        max_dso = count_consecutive(sub_pre['dso_gt45'].values)
        max_fluct = count_consecutive(sub_pre['rev_fluct'].values)
        print(f"{sub}: max cons DSO>45={max_dso}, max cons RevFluc={max_fluct}")