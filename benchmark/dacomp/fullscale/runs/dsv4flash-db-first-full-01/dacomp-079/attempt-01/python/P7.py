import pandas as pd, numpy as np
from scipy import stats

df = pd.read_csv('/work/user_level.csv')
df['tenure_days'] = (pd.to_datetime(df['last_event_on']) - pd.to_datetime(df['first_event_on'])).dt.days
df['segment'] = np.where((df['count_active_days'] > 60) & (df['distinct_features'] < 5), 'single_feature', 'other')

# Retention by segment among heavy users only
heavy = df[df['count_active_days'] > 60].copy()
heavy['seg'] = np.where(heavy['distinct_features'] < 5, 'single', 'multi')
print("Heavy-only retention metrics:")
print(heavy.groupby('seg')[['count_active_months','count_active_days','tenure_days']].mean().round(2).to_string())

# Monthly coverage ratio
heavy['potential_months'] = (heavy['tenure_days']/30).clip(lower=1)
heavy['coverage'] = heavy['count_active_months']/heavy['potential_months']
print("\nMonthly coverage ratio (active_months / potential_months):")
print(heavy.groupby('seg')['coverage'].mean().round(3).to_string())

# Events per active day
df['events_per_day'] = df['sum_events']/df['count_active_days']
print("\nEvents per active day:")
print(df.groupby('segment')['events_per_day'].mean().round(2).to_string())

# Clicks per feature (for single-feature users, how many clicks per feature)
print("\nSingle-feature users: avg clicks per feature")
single = df[df['segment']=='single_feature']
print("  total clicks:", single['sum_events'].mean().round(1))
print("  distinct features:", single['distinct_features'].mean().round(2))
print("  clicks per feature:", (single['sum_events']/single['distinct_features']).mean().round(1))

# Multi-feature heavy users comparison
multi = heavy[heavy['seg']=='multi']
print("\nMulti-feature heavy users:")
print("  total events:", multi['sum_events'].mean().round(1))
print("  distinct features:", multi['distinct_features'].mean().round(2))
print("  events per feature:", (multi['sum_events']/multi['distinct_features']).mean().round(1))

# Statistical test: retention (active months) between single and multi heavy users
a = heavy[heavy['seg']=='single']['count_active_months']
b = heavy[heavy['seg']=='multi']['count_active_months']
print("\nActive months test: single vs multi heavy")
print("  means:", a.mean().round(2), "vs", b.mean().round(2))
print("  MW p =", stats.mannwhitneyu(a,b)[1])

# Tenure days test
a = heavy[heavy['seg']=='single']['tenure_days']
b = heavy[heavy['seg']=='multi']['tenure_days']
print("Tenure days test:")
print("  means:", a.mean().round(1), "vs", b.mean().round(1))
print("  MW p =", stats.mannwhitneyu(a,b)[1])