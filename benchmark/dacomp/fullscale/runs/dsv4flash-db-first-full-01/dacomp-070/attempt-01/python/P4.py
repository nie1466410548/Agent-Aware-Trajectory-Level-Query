import pandas as pd
import numpy as np

# Use db.query to fetch datasets with proper column names
res = db.query("""
SELECT cr.region, dr.device, strftime('%Y-%m', cr.date_day) AS month,
  SUM(cr.store_listing_visitors) AS visitors, SUM(cr.store_listing_acquisitions) AS acquisitions,
  SUM(dr.device_installs) AS installs, SUM(dr.device_uninstalls) AS uninstalls,
  SUM(dr.update_events) AS updates, SUM(dr.active_devices_last_30_days) AS actives,
  AVG(dr.rolling_total_average_rating) AS rating
FROM google_play__country_report cr
JOIN google_play__device_report dr ON cr.date_day = dr.date_day AND cr.package_name = dr.package_name
GROUP BY cr.region, dr.device, month
ORDER BY cr.region, dr.device, month
""")
df_rd = db.frame(res)
df_rd['month_dt'] = pd.to_datetime(df_rd['month'] + '-01')
df_rd['month_num'] = (df_rd['month_dt'] - df_rd['month_dt'].min()).dt.days / 30.0
df_rd['conv_rate'] = 100.0 * df_rd['acquisitions'] / df_rd['visitors']
df_rd['cost_per_acq'] = df_rd['visitors'] / df_rd['acquisitions']
df_rd['installs_per_acq'] = df_rd['installs'] / df_rd['acquisitions']
df_rd['update_rate'] = df_rd['updates'] / df_rd['actives'] * 1000
print("Region×Device:", df_rd.shape)
df_rd.to_csv('/work/region_device_monthly.csv', index=False)

res = db.query("""
SELECT strftime('%Y-%m', cr.date_day) AS month, cr.region, cr.package_name,
  SUM(cr.store_listing_visitors) AS visitors, SUM(cr.store_listing_acquisitions) AS acquisitions,
  SUM(cr.device_installs) AS installs, SUM(cr.update_events) AS updates,
  SUM(cr.active_devices_last_30_days) AS actives,
  AVG(cr.rolling_total_average_rating) AS rating,
  AVG(ts.quality_score) AS quality, AVG(ts.crash_rate_per_1k) AS crash,
  AVG(ts.revenue_per_active_device) AS rpad, AVG(ts.daily_churn_rate) AS churn
FROM google_play__country_report cr
JOIN google_play__time_series_trends ts ON cr.date_day = ts.date_day AND cr.package_name = ts.package_name
GROUP BY month, cr.region, cr.package_name
ORDER BY cr.region, cr.package_name, month
""")
df_rp = db.frame(res)
df_rp['month_dt'] = pd.to_datetime(df_rp['month'] + '-01')
df_rp['month_num'] = (df_rp['month_dt'] - df_rp['month_dt'].min()).dt.days / 30.0
df_rp['conv_rate'] = 100.0 * df_rp['acquisitions'] / df_rp['visitors']
print("Region×Package:", df_rp.shape)
df_rp.to_csv('/work/region_package_monthly.csv', index=False)

res = db.query("""
SELECT strftime('%Y-%m', date_day) AS month, package_name,
  AVG(quality_score) AS quality, AVG(crash_rate_per_1k) AS crash, AVG(anr_rate_per_1k) AS anr,
  AVG(revenue_per_active_device) AS rpad, AVG(active_devices) AS active,
  AVG(ma_7d_quality) AS ma7q, AVG(ma_30d_quality) AS ma30q,
  AVG(wow_install_growth_rate) AS wow_inst, AVG(wow_revenue_growth_rate) AS wow_rev,
  AVG(install_volatility_coefficient) AS inst_vol, AVG(revenue_volatility_coefficient) AS rev_vol
FROM google_play__time_series_trends
GROUP BY month, package_name
ORDER BY package_name, month
""")
df_ts = db.frame(res)
df_ts['month_dt'] = pd.to_datetime(df_ts['month'] + '-01')
df_ts['month_num'] = (df_ts['month_dt'] - df_ts['month_dt'].min()).dt.days / 30.0
print("TimeSeries:", df_ts.shape)
df_ts.to_csv('/work/package_monthly.csv', index=False)
print(df_ts.groupby('package_name')[['wow_inst','wow_rev','active','rpad','quality','crash']].mean().round(4))