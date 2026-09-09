import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

d = pd.read_csv('/work/metrics_all.csv')
d['dashboard_date'] = pd.to_datetime(d['dashboard_date'])

# Pre-high window
pre = d[d['is_prehigh']].copy()
# Healthy = all Low-risk periods
healthy = d[d['cash_flow_risk_level']=='Low'].copy()

print(f"Pre-high observations: {len(pre)}")
print(f"Healthy (Low risk) observations: {len(healthy)}")

# ========== DSO rate of change ==========
pre['dso_mom_chg'] = pre['weighted_average_days_outstanding'] - pre['prev_revenue']  # no, wrong
# Actually compute DSO change
pre['dso_chg'] = pre['weighted_average_days_outstanding'] - pre.groupby('subsidiary_id')['weighted_average_days_outstanding'].shift(1)
# Can't easily compute this in pandas with the already-loaded data. Let me do it differently.
# Re-load with DSO lag
d['prev_dso'] = d.groupby('subsidiary_id')['weighted_average_days_outstanding'].shift(1)
d['dso_chg'] = d['weighted_average_days_outstanding'] - d['prev_dso']
d['dso_chg_pct'] = d['dso_chg'] / d['prev_dso'].abs()
d['overdue_chg'] = d['overdue_percentage'] - d['prev_overdue']

pre = d[d['is_prehigh']].copy()
healthy = d[d['cash_flow_risk_level']=='Low'].copy()

# ========== Threshold testing ==========
print("\n=== THRESHOLD TESTING ===")
# Test various DSO thresholds
for thresh in [30, 35, 40, 45]:
    pre_flag = (pre['weighted_average_days_outstanding'] > thresh).mean()
    healthy_flag = (healthy['weighted_average_days_outstanding'] > thresh).mean()
    print(f"DSO > {thresh:2d}: pre-high={pre_flag:.2%}, healthy={healthy_flag:.2%}")

# DSO change > 10 (sudden jump)
pre['dso_jump10'] = pre['dso_chg'] > 10
healthy['dso_jump10'] = healthy['dso_chg'] > 10
print(f"\nDSO jump >10: pre-high={pre['dso_jump10'].mean():.2%}, healthy={healthy['dso_jump10'].mean():.2%}")

# DSO change > 5
pre['dso_jump5'] = pre['dso_chg'] > 5
healthy['dso_jump5'] = healthy['dso_chg'] > 5
print(f"DSO jump >5: pre-high={pre['dso_jump5'].mean():.2%}, healthy={healthy['dso_jump5'].mean():.2%}")

# Overdue percentage absolute level
for thresh in [5, 7, 10, 15]:
    pre_flag = (pre['overdue_percentage'] > thresh).mean()
    healthy_flag = (healthy['overdue_percentage'] > thresh).mean()
    print(f"Overdue% > {thresh:2d}: pre-high={pre_flag:.2%}, healthy={healthy_flag:.2%}")

# Overdue change > 1pp
pre['overdue_jump1'] = pre['overdue_chg'] > 1
healthy['overdue_jump1'] = healthy['overdue_chg'] > 1
print(f"Overdue jump >1pp: pre-high={pre['overdue_jump1'].mean():.2%}, healthy={healthy['overdue_jump1'].mean():.2%}")

# Expense growth > revenue growth (any extent)
pre['exp_gt_rev'] = pre['exp_chg'] > pre['rev_chg']
healthy['exp_gt_rev'] = healthy['exp_chg'] > healthy['rev_chg']
print(f"\nExpense growth > Rev growth: pre-high={pre['exp_gt_rev'].mean():.2%}, healthy={healthy['exp_gt_rev'].mean():.2%}")

# Expense growth > 0 while revenue growth < 0
pre['exp_up_rev_down'] = (pre['exp_chg'] > 0) & (pre['rev_chg'] < 0)
healthy['exp_up_rev_down'] = (healthy['exp_chg'] > 0) & (healthy['rev_chg'] < 0)
print(f"Expense up, Revenue down: pre-high={pre['exp_up_rev_down'].mean():.2%}, healthy={healthy['exp_up_rev_down'].mean():.2%}")

# Revenue decline > 20%
pre['rev_decline20'] = pre['rev_chg'] < -0.20
healthy['rev_decline20'] = healthy['rev_chg'] < -0.20
print(f"Revenue decline >20%: pre-high={pre['rev_decline20'].mean():.2%}, healthy={healthy['rev_decline20'].mean():.2%}")

# Revenue decline > 10%
pre['rev_decline10'] = pre['rev_chg'] < -0.10
healthy['rev_decline10'] = healthy['rev_chg'] < -0.10
print(f"Revenue decline >10%: pre-high={pre['rev_decline10'].mean():.2%}, healthy={healthy['rev_decline10'].mean():.2%}")

# ========== Best combined early warning ==========
# Let's try various combinations
print("\n=== COMBINATION TESTING ===")
combos = [
    ('DSO > 35', pre['weighted_average_days_outstanding']>35, healthy['weighted_average_days_outstanding']>35),
    ('DSO > 40', pre['weighted_average_days_outstanding']>40, healthy['weighted_average_days_outstanding']>40),
    ('RevFluc >20%', pre['rev_fluct'], healthy['rev_fluct']),
    ('Rev decline >10%', pre['rev_decline10'], healthy['rev_decline10']),
    ('Exp up Rev down', pre['exp_up_rev_down'], healthy['exp_up_rev_down']),
    ('Expense > Revenue growth', pre['exp_gt_rev'], healthy['exp_gt_rev']),
    ('Divergence > 20pp', pre['divergence']>0.20, healthy['divergence']>0.20),
    ('Overdue jump >1pp', pre['overdue_jump1'], healthy['overdue_jump1']),
    ('DSO jump >5', pre['dso_jump5'], healthy['dso_jump5']),
    ('3mo overdue rise', pre['overdue_rise3'], healthy['overdue_rise3']),
]

for name, p_sig, h_sig in combos:
    sens = p_sig.mean()
    spec = 1 - h_sig.mean()
    print(f"  {name:30s}: sensitivity={sens:.2%}, specificity={spec:.2%}")

# Now test 2-signal combinations
print("\n=== 2-SIGNAL COMBINATIONS (ANY) ===")
signals = [
    ('DSO>35', pre['weighted_average_days_outstanding']>35, healthy['weighted_average_days_outstanding']>35),
    ('RevFluc>20%', pre['rev_fluct'], healthy['rev_fluct']),
    ('ExpUpRevDown', pre['exp_up_rev_down'], healthy['exp_up_rev_down']),
    ('OverdueJump1pp', pre['overdue_jump1'], healthy['overdue_jump1']),
    ('DSOjump5', pre['dso_jump5'], healthy['dso_jump5']),
]

from itertools import combinations
for (n1, p1, h1), (n2, p2, h2) in combinations(signals, 2):
    sens = (p1 | p2).mean()
    spec = 1 - (h1 | h2).mean()
    print(f"  {n1} OR {n2}: sensitivity={sens:.2%}, specificity={spec:.2%}")

# 3-signal combinations
print("\n=== 3-SIGNAL COMBINATIONS (ANY 2 OF 3) ===")
for (n1, p1, h1), (n2, p2, h2), (n3, p3, h3) in combinations(signals, 3):
    any2 = (p1.astype(int) + p2.astype(int) + p3.astype(int)) >= 2
    any2_h = (h1.astype(int) + h2.astype(int) + h3.astype(int)) >= 2
    sens = any2.mean()
    spec = 1 - any2_h.mean()
    print(f"  Any 2 of {n1},{n2},{n3}: sensitivity={sens:.2%}, specificity={spec:.2%}")

# ========== EARLY WARNING: 2-3 months before High ==========
print("\n=== EARLY WARNING (2-3 months before High) ===")
# Get the periods that are 2-3 months before High
d['months_to_high'] = d['first_high_idx'] - d['period_idx']
early = d[(d['months_to_high']>=2) & (d['months_to_high']<=4)].copy()  # ~2-4 months before
late = d[(d['months_to_high']>=0) & (d['months_to_high']<=1)].copy()   # 0-1 months before

print(f"Early (2-4mo before): {len(early)} obs")
print(f"Late (0-1mo before): {len(late)} obs")

# Key metrics in early warning window
print("\nEarly warning window (2-4 months before High):")
print(f"  DSO > 35: {((early['weighted_average_days_outstanding']>35).mean()):.2%}")
print(f"  RevFluc >20%: {(early['rev_fluct'].mean()):.2%}")
print(f"  Expense up, Rev down: {((early['exp_chg']>0) & (early['rev_chg']<0)).mean():.2%}")
print(f"  Overdue jump >1pp: {((early['overdue_percentage']-early['prev_overdue'])>1).mean():.2%}")
print(f"  Mean DSO: {early['weighted_average_days_outstanding'].mean():.1f}")
print(f"  Mean overdue%: {early['overdue_percentage'].mean():.1f}")

# ========== VISUALIZATION ==========
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 1. DSO trajectory by subsidiary
for sub in d['subsidiary_id'].unique():
    s = d[d['subsidiary_id']==sub].sort_values('period_idx')
    pre_mask = s['is_prehigh']
    axes[0,0].plot(s['period_idx'], s['weighted_average_days_outstanding'], 
                   marker='o', alpha=0.5, label=sub[-4:])
axes[0,0].axhline(45, color='red', linestyle='--', alpha=0.5, label='DSO=45')
axes[0,0].axhline(35, color='orange', linestyle=':', alpha=0.5, label='DSO=35')
axes[0,0].set_title('DSO Trajectory by Subsidiary')
axes[0,0].set_xlabel('Period Index')
axes[0,0].set_ylabel('Days Outstanding')
axes[0,0].legend(fontsize=6, ncol=2)

# 2. Overdue% trajectory
for sub in d['subsidiary_id'].unique():
    s = d[d['subsidiary_id']==sub].sort_values('period_idx')
    axes[0,1].plot(s['period_idx'], s['overdue_percentage'], 
                   marker='o', alpha=0.5, label=sub[-4:])
axes[0,1].set_title('Overdue % Trajectory')
axes[0,1].set_xlabel('Period Index')
axes[0,1].set_ylabel('Overdue %')

# 3. Revenue and expense by months-to-high
mt = d[(d['months_to_high']>=0) & (d['months_to_high']<=7)].groupby('months_to_high').agg(
    rev_mean=('revenue','mean'),
    exp_mean=('expense','mean')
).reset_index().sort_values('months_to_high', ascending=False)
axes[0,2].plot(mt['months_to_high'], mt['rev_mean']/1e6, 'o-', color='green', label='Revenue')
axes[0,2].plot(mt['months_to_high'], mt['exp_mean']/1e6, 's-', color='red', label='Expense')
axes[0,2].set_title('Revenue & Expense by Months-to-High')
axes[0,2].set_xlabel('Months Before High')
axes[0,2].set_ylabel('Amount ($M)')
axes[0,2].legend()
axes[0,2].invert_xaxis()

# 4. Combined signal comparison
groups = ['Pre-High\n(6mo)', 'Healthy\n(Low risk)']
metrics = [
    ('Revenue Fluct >20%', [pre['rev_fluct'].mean(), healthy['rev_fluct'].mean()]),
    ('DSO > 35', [(pre['weighted_average_days_outstanding']>35).mean(), (healthy['weighted_average_days_outstanding']>35).mean()]),
    ('Exp up, Rev down', [pre['exp_up_rev_down'].mean(), healthy['exp_up_rev_down'].mean()]),
    ('Overdue jump >1pp', [pre['overdue_jump1'].mean(), healthy['overdue_jump1'].mean()]),
]
x = range(len(metrics))
width = 0.35
for i, (name, vals) in enumerate(metrics):
    axes[1,0].bar(i-width/2, vals[0], width, color='crimson', alpha=0.7)
    axes[1,0].bar(i+width/2, vals[1], width, color='forestgreen', alpha=0.7)
axes[1,0].set_xticks(range(len(metrics)))
axes[1,0].set_xticklabels([m[0] for m in metrics], rotation=15, ha='right')
axes[1,0].set_title('Signal Rates: Pre-High vs Healthy')
axes[1,0].legend(['Pre-High', 'Healthy'])

# 5. Divergence by months-to-high
div_mt = d[(d['months_to_high']>=0) & (d['months_to_high']<=7)].groupby('months_to_high')['divergence'].mean()
axes[1,1].plot(div_mt.index, div_mt.values, 'o-', color='purple')
axes[1,1].axhline(0, color='grey', linestyle='--', alpha=0.5)
axes[1,1].set_title('Expense-Revenue Divergence by Months-to-High')
axes[1,1].set_xlabel('Months Before High')
axes[1,1].set_ylabel('Expense Growth - Revenue Growth (pp)')
axes[1,1].invert_xaxis()

# 6. Heatmap of signal strength
ax = axes[1,2]
signal_data = []
for name, p_sig, h_sig in combos[:8]:
    signal_data.append([name, p_sig.mean(), 1-h_sig.mean()])
sig_df = pd.DataFrame(signal_data, columns=['signal','sensitivity','specificity'])
sig_df.plot.barh(x='signal', ax=ax, legend=False)
ax.set_title('Signal Strength (Sensitivity & Specificity)')
ax.set_xlabel('Rate')
plt.tight_layout()
plt.savefig('/work/early_warning_analysis.png', dpi=120)
print("Saved early_warning_analysis.png")