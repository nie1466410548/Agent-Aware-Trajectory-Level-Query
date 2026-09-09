
import numpy as np, pandas as pd
from scipy import stats

daily = pd.read_csv('/work/daily_stats.csv')
daily['date'] = pd.to_datetime(daily['date_key'])
daily['cancel_pct'] = 100*daily['cancellations']/daily['bookings']
daily['nodriver_pct'] = 100*daily['no_driver']/daily['bookings']
daily['incomplete_pct'] = 100*daily['incomplete']/daily['bookings']
daily['weekday'] = daily['date'].dt.dayofweek  # 0=Mon
daily['month'] = daily['date'].dt.month

# Correlations between daily volume and metrics
print("=== Pearson correlations (daily, N=%d) ===" % len(daily))
for col in ['cancel_pct','nodriver_pct','incomplete_pct','cost_per_km']:
    r, p = stats.pearsonr(daily['bookings'], daily[col])
    print("%-16s r=%.3f  p=%.4f" % (col, r, p))

# Top/bottom decile comparison
q_hi = daily['bookings'].quantile(0.9); q_lo = daily['bookings'].quantile(0.1)
hi = daily[daily['bookings']>=q_hi]; lo = daily[daily['bookings']<=q_lo]
print("\n=== Top-decile volume days (>=%.0f bookings, n=%d) vs bottom-decile (<=%.0f, n=%d) ===" % (q_hi,len(hi),q_lo,len(lo)))
comp = pd.DataFrame({
    'Metric': ['bookings','cancel_pct','nodriver_pct','incomplete_pct','cost_per_km'],
    'High-volume days': [hi['bookings'].mean(), hi['cancel_pct'].mean(), hi['nodriver_pct'].mean(), hi['incomplete_pct'].mean(), hi['cost_per_km'].mean()],
    'Low-volume days': [lo['bookings'].mean(), lo['cancel_pct'].mean(), lo['nodriver_pct'].mean(), lo['incomplete_pct'].mean(), lo['cost_per_km'].mean()],
})
print(comp.round(3).to_string(index=False))

# Weekday per-km cost and distance - query needed for distance
print("\nWeekday profiles from daily data:")
wd = daily.groupby('weekday').agg(bookings=('bookings','mean'), cancel_pct=('cancel_pct','mean'),
                                  cost_per_km=('cost_per_km','mean')).round(3)
print(wd.to_string())

# T-test: weekend vs weekday per-km cost
daily['is_weekend'] = daily['weekday'].isin([5,6])
w = daily[daily['is_weekend']]['cost_per_km']; nw = daily[~daily['is_weekend']]['cost_per_km']
t, p = stats.ttest_ind(w.dropna(), nw.dropna())
print("\nWeekend per-km cost: %.2f +/- %.2f ; Weekday: %.2f +/- %.2f ; t=%.2f p=%.4f" % (
    w.mean(), w.std(), nw.mean(), nw.std(), t, p))

# Weekly pattern of cancellation by weekday (daily)
print("\nMean daily cancel_pct by weekday:")
print(daily.groupby('weekday')['cancel_pct'].mean().round(2).to_string())
