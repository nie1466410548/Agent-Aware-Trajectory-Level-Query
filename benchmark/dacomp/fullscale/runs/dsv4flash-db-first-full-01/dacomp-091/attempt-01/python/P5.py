import pandas as pd
import numpy as np

df = pd.read_csv('/work/per_pair_gl_data.csv')
df['raw_change_pct'] = np.where(df['raw_prior12'].abs() > 0,
    (df['raw_last12'] - df['raw_prior12'])/df['raw_prior12'].abs()*100, np.nan)
df['mag_change_pct'] = np.where(df['mag_prior12'] > 0,
    (df['mag_last12'] - df['mag_prior12'])/df['mag_prior12']*100, np.nan)
df['tx_freq_density'] = df['n_tx']/df['n_active_days']

stats = df.groupby('account_type').agg(
    n_pairs=('vendor_id','count'),
    avg_change=('mag_change_pct','mean'),
    median_change=('mag_change_pct','median'),
    p25=('mag_change_pct', lambda s: s.quantile(0.25)),
    p75=('mag_change_pct', lambda s: s.quantile(0.75)),
    avg_freq=('tx_freq_density','mean'),
    median_freq=('tx_freq_density','median'),
    min_freq=('tx_freq_density','min'),
    max_freq=('tx_freq_density','max'),
    total_vol_last12=('mag_last12','sum'),
    total_vol_prior12=('mag_prior12','sum')
)
stats['total_vol_change_pct'] = (stats['total_vol_last12']-stats['total_vol_prior12'])/stats['total_vol_prior12']*100
pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 20)
print(stats.round(4).to_string())

# Also vendor-level risk tiering stats
r2 = db.query("""
  SELECT vendor_tier, payment_risk_level, performance_rating, recommended_strategy, dependency_level, COUNT(*) AS n
  FROM quickbooks__vendor_performance
  WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
  GROUP BY vendor_tier, payment_risk_level, performance_rating, recommended_strategy, dependency_level
  ORDER BY n DESC
""")
from collections import defaultdict
agg = defaultdict(int)
for row in db.rows(r2):
    for k in ['vendor_tier','payment_risk_level','performance_rating','dependency_level']:
        agg[(k, row[k])] += row['n']
print("\n=== Categorical distribution of selected vendors ===")
for k in ['vendor_tier','payment_risk_level','performance_rating','dependency_level']:
    print(k)
    for (kk, v), n in sorted(agg.items(), key=lambda x: -x[1]):
        if kk == k:
            print(f"  {v}: {n}")