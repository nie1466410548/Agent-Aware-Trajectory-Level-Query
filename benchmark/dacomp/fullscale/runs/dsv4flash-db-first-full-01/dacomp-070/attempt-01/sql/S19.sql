
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
