
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

cols = ["visitor_id","count_active_days","count_active_months","average_daily_minutes",
        "average_daily_events","latest_nps_rating","sum_minutes","sum_events",
        "first_event_on","last_event_on","account_avg_nps","distinct_features"]

rows = []
with open('/results/S34.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df = pd.DataFrame(rows, columns=cols)

df['segment'] = np.where((df['count_active_days'] > 60) & (df['distinct_features'] < 5), 'single_feature', 'other')
df['segment_heavy'] = np.where(df['count_active_days'] > 60,
                               np.where(df['distinct_features'] < 5, 'single_feature_heavy', 'multi_feature_heavy'),
                               'low_activity')

print("Segment sizes (all users):")
print(df['segment'].value_counts())
print("Share single-feature among all:", (df['segment']=='single_feature').mean().round(4))

# NPS check
for seg in ['single_feature','other']:
    sub = df[df['segment']==seg]
    print(seg, 'avg latest_nps:', sub['latest_nps_rating'].mean().round(3), 'n=', len(sub))

# Statistical tests: average_daily_minutes
a = df[df['segment']=='single_feature']['average_daily_minutes'].dropna()
b = df[df['segment']=='other']['average_daily_minutes'].dropna()
u, p = stats.mannwhitneyu(a, b, alternative='two-sided')
t, pt = stats.ttest_ind(a, b, equal_var=False)
print("\nMann-Whitney avg_daily_minutes p =", p)
print("Welch t avg_daily_minutes: t =", t.round(3), "p =", pt)

# Among heavy users only
a2 = df[df['segment_heavy']=='single_feature_heavy']['average_daily_minutes'].dropna()
b2 = df[df['segment_heavy']=='multi_feature_heavy']['average_daily_minutes'].dropna()
u2, p2 = stats.mannwhitneyu(a2, b2)
t2, pt2 = stats.ttest_ind(a2, b2, equal_var=False)
print("\nHeavy-only: avg_daily_minutes single vs multi")
print("  means:", a2.mean().round(2), "vs", b2.mean().round(2))
print("  Mann-Whitney p =", p2, "| Welch t =", t2.round(3), "p =", pt2)

# NPS tests
nps_a = df[df['segment']=='single_feature']['latest_nps_rating'].dropna()
nps_b = df[df['segment']=='other']['latest_nps_rating'].dropna()
print("\nNPS means:", nps_a.mean().round(3), "vs", nps_b.mean().round(3))
print("Mann-Whitney NPS p =", stats.mannwhitneyu(nps_a, nps_b)[1])

# average_daily_events
ev_a = df[df['segment']=='single_feature']['average_daily_events'].dropna()
ev_b = df[df['segment']=='other']['average_daily_events'].dropna()
print("\nDaily events means:", ev_a.mean().round(3), "vs", ev_b.mean().round(3),
      "| MW p =", stats.mannwhitneyu(ev_a, ev_b)[1])

# minutes per event
df['min_per_event'] = df['sum_minutes'] / df['sum_events'].replace(0, np.nan)
mpa = df[df['segment']=='single_feature']['min_per_event'].dropna()
mpb = df[df['segment']=='other']['min_per_event'].dropna()
print("\nMinutes per event:", mpa.mean().round(3), "vs", mpb.mean().round(3),
      "| MW p =", stats.mannwhitneyu(mpa, mpb)[1])

# Active days & months
print("\nActive days means:", df[df['segment']=='single_feature']['count_active_days'].mean().round(1),
      "vs", df[df['segment']=='other']['count_active_days'].mean().round(1))
print("Active months means:", df[df['segment']=='single_feature']['count_active_months'].mean().round(2),
      "vs", df[df['segment']=='other']['count_active_months'].mean().round(2))
span_a = (pd.to_datetime(df[df['segment']=='single_feature']['last_event_on']) - pd.to_datetime(df[df['segment']=='single_feature']['first_event_on'])).dt.days
span_b = (pd.to_datetime(df[df['segment']=='other']['last_event_on']) - pd.to_datetime(df[df['segment']=='other']['first_event_on'])).dt.days
print("Tenure span days:", span_a.mean().round(1), "vs", span_b.mean().round(1))

df.to_csv('/work/user_level.csv', index=False)
print("\nSaved /work/user_level.csv")
