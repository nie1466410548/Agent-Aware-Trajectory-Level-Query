SELECT strftime('%Y-%m', cr.date_day) AS month, cr.region, cr.package_name,
  SUM(cr.store_listing_visitors) AS visitors, SUM(cr.store_listing_acquisitions) AS acquisitions,
  ROUND(100.0*SUM(cr.store_listing_acquisitions)/NULLIF(SUM(cr.store_listing_visitors),0),4) AS conv_rate,
  SUM(cr.device_installs) AS installs, SUM(cr.update_events) AS updates,
  SUM(cr.active_devices_last_30_days) AS actives,
  ROUND(AVG(cr.rolling_total_average_rating),4) AS rating,
  ROUND(AVG(ts.quality_score),4) AS quality, ROUND(AVG(ts.crash_rate_per_1k),4) AS crash,
  ROUND(AVG(ts.revenue_per_active_device),8) AS rpad, ROUND(AVG(ts.daily_churn_rate),5) AS churn,
  SUM(cr.store_listing_acquisitions) AS acq
FROM google_play__country_report cr
JOIN google_play__time_series_trends ts ON cr.date_day = ts.date_day AND cr.package_name = ts.package_name
GROUP BY month, cr.region, cr.package_name
ORDER BY cr.region, cr.package_name, month