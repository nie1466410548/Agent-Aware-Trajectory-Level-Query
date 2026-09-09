import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

d = pd.read_csv('/work/metrics_all.csv')
d['dashboard_date'] = pd.to_datetime(d['dashboard_date'])
d['months_to_high'] = d['first_high_idx'] - d['period_idx']
d['prev_dso'] = d.groupby('subsidiary_id')['weighted_average_days_outstanding'].shift(1)
d['dso_chg'] = d['weighted_average_days_outstanding'] - d['prev_dso']
d['overdue_chg'] = d['overdue_percentage'] - d['prev_overdue']

healthy = d[d['cash_flow_risk_level']=='Low'].copy()
ew = d[(d['months_to_high']==2) | (d['months_to_high']==3)].copy()

def evald(sig_expr, df):
    return df.eval(sig_expr).fillna(False)

combos = [
    ('DSO>35 OR RevFluc>20%', 'weighted_average_days_outstanding>35', 'rev_fluct'),
    ('DSO>35 OR RevDecline>10%', 'weighted_average_days_outstanding>35', 'rev_chg<-0.10'),
    ('DSO>35 OR Exp>Rev', 'weighted_average_days_outstanding>35', 'exp_chg>rev_chg'),
    ('DSO>35 OR DSOjump>5', 'weighted_average_days_outstanding>35', 'dso_chg>5'),
    ('RevFluc>20% OR DSOjump>5', 'rev_fluct', 'dso_chg>5'),
    ('RevFluc>20% OR Exp>Rev', 'rev_fluct', 'exp_chg>rev_chg'),
]
print("=== Combinations in 2-3 month EARLY WARNING window ===")
for name, e1, e2 in combos:
    p = evald(e1, ew) | evald(e2, ew)
    h = evald(e1, healthy) | evald(e2, healthy)
    print(f"{name:45s} sens={p.mean():.2%}, spec={1-h.mean():.2%}")

# Strict: DSO>35 AND (RevFluc OR DSOjump)
p_strict = evald('weighted_average_days_outstanding>35', ew) & (evald('rev_fluct', ew) | evald('dso_chg>5', ew))
h_strict = evald('weighted_average_days_outstanding>35', healthy) & (evald('rev_fluct', healthy) | evald('dso_chg>5', healthy))
print(f"{'DSO>35 AND (RevFluc OR DSOjump)':45s} sens={p_strict.mean():.2%}, spec={1-h_strict.mean():.2%}")

# Score >= 2 in early warning
def score_flag(df):
    return ((df['weighted_average_days_outstanding']>35).fillna(False).astype(int) + 
            df['rev_fluct'].fillna(False).astype(int) + 
            (df['overdue_chg']>1).fillna(False).astype(int) + 
            (df['exp_chg']>df['rev_chg']).fillna(False).astype(int))
for th in [2,3]:
    s = (score_flag(ew)>=th).mean()
    sp = 1-(score_flag(healthy)>=th).mean()
    print(f"Score >= {th}: sens={s:.2%}, spec={sp:.2%}")

# ============ FINAL FIGURE ============
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

results = [
    ('DSO > 35', 0.50, 1.00),
    ('DSO > 40', 0.30, 1.00),
    ('Rev Fluct >20%', 0.45, 0.65),
    ('Rev decline >10%', 0.45, 0.70),
    ('Exp growth > Rev growth', 0.50, 0.57),
    ('DSO jump > 5', 0.45, 0.92),
    ('Overdue jump >1pp', 0.20, 0.70),
    ('3mo overdue rise', 0.05, 0.92),
]
ax = axes[0]
names = [r[0] for r in results]
sens = [r[1] for r in results]
spec = [r[2] for r in results]
x = np.arange(len(names))
ax.bar(x-0.2, sens, 0.4, label='Sensitivity (2-3mo before High)', color='crimson', alpha=0.8)
ax.bar(x+0.2, spec, 0.4, label='Specificity (Healthy)', color='forestgreen', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(names, rotation=25, ha='right', fontsize=8)
ax.set_ylabel('Rate')
ax.set_title('Signal Strength in the 2-3 Month Early-Warning Window')
ax.legend(fontsize=8)
ax.set_ylim(0, 1.05)

ax = axes[1]
framework = [
    ['Tier 1 - ALERT', 'DSO > 35 days', 'sens 50% / spec 100%'],
    ['Tier 1 - ALERT', 'Rev MoM fluctuation > 20%', 'sens 43% / spec 65%'],
    ['Tier 2 - ESCALATE', 'DSO>35 AND (RevFluc>20% OR DSO jump>5)', 'sens 35% / spec 100%'],
    ['Tier 2 - ESCALATE', 'Composite score >= 3 of 4 signals', 'sens 20% / spec 97%'],
    ['Tier 3 - CRISIS', 'DSO > 45 OR Overdue% > 10%', 'concurrent (transition month)'],
]
ax.axis('off')
ax.set_title('Recommended 2-3 Month Cash-Flow Crisis Early-Warning Framework', fontsize=10)
tbl = ax.table(cellText=framework, colLabels=['Tier', 'Trigger Rule', 'Performance'],
               loc='center', cellLoc='left')
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1, 1.8)
plt.tight_layout()
plt.savefig('/work/final_framework.png', dpi=120)
print("Saved final_framework.png")

# Lead time verification
lead = []
for sub in d['subsidiary_id'].unique():
    s = d[(d['subsidiary_id']==sub) & d['is_prehigh']].sort_values('period_idx')
    f = s[s['weighted_average_days_outstanding']>35]
    if len(f):
        lead.append(int(f.iloc[0]['months_to_high']))
print(f"\nDSO>35 first-fire lead time: median {int(np.median(lead))} months, range {min(lead)}-{max(lead)} months")

lead2 = []
for sub in d['subsidiary_id'].unique():
    s = d[(d['subsidiary_id']==sub) & d['is_prehigh']].sort_values('period_idx')
    sc = ((s['weighted_average_days_outstanding']>35).fillna(False).astype(int) + s['rev_fluct'].fillna(False).astype(int)).astype(bool)
    f = s[sc]
    if len(f):
        lead2.append(int(f.iloc[0]['months_to_high']))
print(f"DSO>35 OR RevFluc first-fire lead time: median {int(np.median(lead2))} months, range {min(lead2)}-{max(lead2)} months")
