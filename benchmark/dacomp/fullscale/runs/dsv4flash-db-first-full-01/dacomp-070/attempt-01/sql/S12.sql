SELECT strftime('%Y-%m', date_day) AS month, region, 
  ROUND(100.0*SUM(store_listing_acquisitions)/NULLIF(SUM(store_listing_visitors),0),3) AS conv_rate,
  ROUND(1.0*SUM(store_listing_visitors)/NULLIF(SUM(store_listing_acquisitions),0),2) AS cost_per_acq_visitors,
  ROUND(1.0*SUM(device_installs)/NULLIF(SUM(store_listing_acquisitions),0),3) AS installs_per_acq,
  SUM(update_events) AS updates,
  SUM(active_devices_last_30_days) AS actives,
  ROUND(AVG(rolling_total_average_rating),3) AS avg_rating
FROM google_play__country_report
GROUP BY month, region 
ORDER BY region, month