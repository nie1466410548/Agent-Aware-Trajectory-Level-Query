import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('/work/contact_funnel.csv')
df['first_response_at'] = pd.to_datetime(df['first_response_at'])
df['demo_booked_at'] = pd.to_datetime(df['demo_booked_at'])
df['trial_activated_at'] = pd.to_datetime(df['trial_activated_at'])
df['paid_at'] = pd.to_datetime(df['paid_at'])

bot = df[df['first_type']=='bot_first']
human = df[df['first_type']=='human_first']

# ============ Chi-square tests for conversion rates ============
print("="*70)
print("STATISTICAL TESTS - CONVERSION RATES")
print("="*70)

def chi2_test(sub, col):
    b = sub[sub['first_type']=='bot_first']
    h = sub[sub['first_type']=='human_first']
    table = np.array([[b[col].sum(), len(b)-b[col].sum()],
                      [h[col].sum(), len(h)-h[col].sum()]])
    chi2, p, dof, _ = stats.chi2_contingency(table)
    return chi2, p

print("\n-- Overall --")
for col, name in [('reached_demo','Demo'), ('reached_trial','Trial'), ('reached_paid','Paid')]:
    chi2, p = chi2_test(df, col)
    print(f"  {name}: chi2={chi2:.3f}, p={p:.4f} {'***' if p<0.05 else ''}")

print("\n-- Conditional funnel rates (proper denominators) --")
# Demo rate among all, trial among demo, paid among trial
def funnel_table(sub, a, b):
    # a: earlier milestone indicator, b: later milestone indicator
    ba = sub[(sub['first_type']=='bot_first') & (sub[a]==1)]
    ha = sub[(sub['first_type']=='human_first') & (sub[a]==1)]
    if len(ba)==0 or len(ha)==0: return None
    table = np.array([[ba[b].sum(), len(ba)-ba[b].sum()],
                      [ha[b].sum(), len(ha)-ha[b].sum()]])
    return table

t = funnel_table(df, 'reached_demo', 'reached_trial')
if t is not None:
    chi2, p, _, _ = stats.chi2_contingency(t)
    print(f"  Trial|Demo: chi2={chi2:.3f}, p={p:.4f} {t.tolist()}")
t = funnel_table(df, 'reached_trial', 'reached_paid')
if t is not None:
    chi2, p, _, _ = stats.chi2_contingency(t)
    print(f"  Paid|Trial: chi2={chi2:.3f}, p={p:.4f} {t.tolist()}")

# Region-level significance
print("\n-- By Region (Paid|Trial) --")
for region in df['region'].unique():
    sub = df[df['region']==region]
    t = funnel_table(sub, 'reached_trial', 'reached_paid')
    if t is not None:
        chi2, p, _, _ = stats.chi2_contingency(t)
        bt = sub[(sub['first_type']=='bot_first') & (sub['reached_trial']==1)]
        ht = sub[(sub['first_type']=='human_first') & (sub['reached_trial']==1)]
        print(f"  {region:25s}: bot={bt['reached_paid'].mean()*100:.1f}% (n={len(bt)}), human={ht['reached_paid'].mean()*100:.1f}% (n={len(ht)}), p={p:.3f}")

print("\n-- By Region (Trial|Demo) --")
for region in df['region'].unique():
    sub = df[df['region']==region]
    t = funnel_table(sub, 'reached_demo', 'reached_trial')
    if t is not None:
        chi2, p, _, _ = stats.chi2_contingency(t)
        bd = sub[(sub['first_type']=='bot_first') & (sub['reached_demo']==1)]
        hd = sub[(sub['first_type']=='human_first') & (sub['reached_demo']==1)]
        print(f"  {region:25s}: bot={bd['reached_trial'].mean()*100:.1f}% (n={len(bd)}), human={hd['reached_trial'].mean()*100:.1f}% (n={len(hd)}), p={p:.3f}")

# Topic-level
print("\n-- By Topic --")
for topic in df['topic'].unique():
    sub = df[df['topic']==topic]
    if len(sub)<50: continue
    bt = sub[(sub['first_type']=='bot_first') & (sub['reached_trial']==1)]
    ht = sub[(sub['first_type']=='human_first') & (sub['reached_trial']==1)]
    t = funnel_table(sub, 'reached_trial', 'reached_paid')
    if t is not None:
        chi2, p, _, _ = stats.chi2_contingency(t)
        print(f"  {topic:10s}: bot paid|trial={bt['reached_paid'].mean()*100:.1f}%, human={ht['reached_paid'].mean()*100:.1f}%, p={p:.3f}")

# ============ Duration tests ============
print("\n" + "="*70)
print("STATISTICAL TESTS - DURATIONS")
print("="*70)

def dur_test(sub, a, b):
    bd = sub[(sub['first_type']=='bot_first') & sub[a].notna() & sub[b].notna()]
    hd = sub[(sub['first_type']=='human_first') & sub[a].notna() & sub[b].notna()]
    d_bot = ((bd[b]-bd[a]).dt.total_seconds()/86400)
    d_hum = ((hd[b]-hd[a]).dt.total_seconds()/86400)
    d_bot = d_bot[d_bot>=0]
    d_hum = d_hum[d_hum>=0]
    if len(d_bot)<5 or len(d_hum)<5:
        return None
    stat, p = stats.mannwhitneyu(d_bot, d_hum, alternative='two-sided')
    return d_bot, d_hum, stat, p

for a, b, name in [('first_response_at','demo_booked_at','FirstResp->Demo'),
                   ('demo_booked_at','trial_activated_at','Demo->Trial'),
                   ('trial_activated_at','paid_at','Trial->Paid')]:
    res = dur_test(df, a, b)
    if res is not None:
        d_bot, d_hum, stat, p = res
        print(f"  {name:15s}: bot mean={d_bot.mean():6.1f}d median={d_bot.median():6.1f}d (n={len(d_bot)}) | human mean={d_hum.mean():6.1f}d median={d_hum.median():6.1f}d (n={len(d_hum)}) | MW p={p:.4f}")

# ============ Response time test ============
print("\n-- First response time (minutes) --")
rt_b = bot['first_response_mins'].dropna()
rt_h = human['first_response_mins'].dropna()
stat, p = stats.mannwhitneyu(rt_b, rt_h, alternative='two-sided')
print(f"  bot mean={rt_b.mean():.1f}, human mean={rt_h.mean():.1f}, p={p:.4f}")