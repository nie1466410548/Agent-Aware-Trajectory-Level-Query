
import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('/work/user_level.csv')
df['segment'] = np.where((df['count_active_days'] > 60) & (df['distinct_features'] < 5), 'single_feature', 'other')

# Bin by active days and compare average_daily_minutes within bins
bins = [0, 30, 60, 90, 120, 150, 200, 1000]
df['day_bin'] = pd.cut(df['count_active_days'], bins=bins)
print("Average daily minutes by active-day bin and segment:")
pivot = df.groupby(['day_bin','segment'], observed=True)['average_daily_minutes'].agg(['mean','count'])
print(pivot.round(2).to_string())
print()

# Within-day-bin Wilcoxon/t-test for daily minutes
print("Per-bin Mann-Whitney tests (single_feature vs other):")
for b in df['day_bin'].cat.categories:
    sub = df[df['day_bin']==b]
    a = sub.loc[sub['segment']=='single_feature','average_daily_minutes'].dropna()
    c = sub.loc[sub['segment']=='other','average_daily_minutes'].dropna()
    if len(a)>10 and len(c)>10:
        u,p = stats.mannwhitneyu(a,c)
        print(f"  {b}: n_single={len(a)}, n_other={len(c)}, means {a.mean():.1f} vs {c.mean():.1f}, p={p:.3e}")

# Retention correlation
print("\nCorrelations with distinct_features (full population):")
print("  active_days:", df['distinct_features'].corr(df['count_active_days']).round(3))
print("  active_months:", df['distinct_features'].corr(df['count_active_months']).round(3))
print("  daily_minutes:", df['distinct_features'].corr(df['average_daily_minutes']).round(3))
print("  nps:", df['distinct_features'].corr(df['latest_nps_rating']).round(3))

# Retention by segment among heavy users only
heavy = df[df['count_active_days'] > 60].copy()
heavy['seg'] = np.where(heavy['distinct_features'] < 5, 'single', 'multi')
print("\nHeavy-only retention metrics:")
print(heavy.groupby('seg')[['count_active_months','count_active_days','tenure_days']].mean().round(2).to_string())

# Monthly coverage ratio (active_months / months of tenure)
heavy['potential_months'] = (heavy['tenure_days']/30).clip(lower=1)
heavy['coverage'] = heavy['count_active_months']/heavy['potential_months']
print(heavy.groupby('seg')['coverage'].mean().round(3).to_string())

# Check: does the single-feature group show a "high return frequency but shallow use" signature?
print("\nEvents per active day (sum_events/count_active_days):")
df['events_per_day'] = df['sum_events']/df['count_active_days']
print(df.groupby('segment')['events_per_day'].mean().round(2).to_string())
