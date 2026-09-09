import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# Load per-pair GL data for selected vendors (raw and magnitude variants)
r = db.query("""
  SELECT vendor_id, account_type,
    SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) AS raw_last12,
    SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) AS raw_prior12,
    SUM(CASE WHEN transaction_date >= '2024-10-15' THEN ABS(amount) ELSE 0 END) AS mag_last12,
    SUM(CASE WHEN transaction_date < '2024-10-15' THEN ABS(amount) ELSE 0 END) AS mag_prior12,
    COUNT(*) AS n_tx,
    COUNT(DISTINCT transaction_date) AS n_active_days
  FROM quickbooks__general_ledger
  WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance
                      WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
  GROUP BY vendor_id, account_type
""")
df = db.frame(r)
df['raw_change_pct'] = np.where(df['raw_prior12'].abs() > 0,
    (df['raw_last12'] - df['raw_prior12'])/df['raw_prior12'].abs()*100, np.nan)
df['mag_change_pct'] = np.where(df['mag_prior12'] > 0,
    (df['mag_last12'] - df['mag_prior12'])/df['mag_prior12']*100, np.nan)
df['tx_freq_density'] = df['n_tx']/df['n_active_days']

print("=== Per-pair magnitude-based spend change rate by account type ===")
stats = df.groupby('account_type').agg(
    n_pairs=('vendor_id','count'),
    avg_change=('mag_change_pct','mean'),
    median_change=('mag_change_pct','median'),
    p25=('mag_change_pct', lambda s: s.quantile(0.25)),
    p75=('mag_change_pct', lambda s: s.quantile(0.75)),
    avg_freq=('tx_freq_density','mean'),
    median_freq=('tx_freq_density','median'),
    total_vol_last12=('mag_last12','sum'),
    total_vol_prior12=('mag_prior12','sum')
).round(4)
print(stats)

# Overall volume change
print("\n=== Overall magnitude-based spend volume (all account types) ===")
print(f"Total volume last12: {df['mag_last12'].sum():,.2f}")
print(f"Total volume prior12: {df['mag_prior12'].sum():,.2f}")
print(f"Overall volume change: {(df['mag_last12'].sum()-df['mag_prior12'].sum())/df['mag_prior12'].sum()*100:.2f}%")

# Net outflow change for expense+liability (the true vendor spend outflows)
out = df[df['account_type'].isin(['Expense','Liability'])]
print("\n=== Net outflow change (Expense+Liability, raw negative sums) ===")
raw_last = out['raw_last12'].sum()
raw_prior = out['raw_prior12'].sum()
print(f"Raw outflow last12: {raw_last:,.2f}")
print(f"Raw outflow prior12: {raw_prior:,.2f}")
print(f"Change: {(raw_last - raw_prior)/abs(raw_prior)*100:.2f}%")

# Save summary for report
df.to_csv('/work/per_pair_gl_data.csv', index=False)
print("\nSaved per-pair data to /work/per_pair_gl_data.csv")