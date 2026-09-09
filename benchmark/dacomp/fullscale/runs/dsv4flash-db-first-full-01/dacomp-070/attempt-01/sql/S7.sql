SELECT strftime('%Y-%m', date_day) AS month, region, COUNT(*) AS n,
  SUM(store_listing_visitors) AS visitors, SUM(store_listing_acquisitions) AS acquisitions,
  ROUND(100.0*SUM(store_listing_acquisitions)/NULLIF(SUM(store_listing_visitors),0),3) AS conv,
  SUM(device_installs) AS installs, SUM(device_uninstalls) AS uninstalls,
  SUM(update_events) AS updates, SUM(active_devices_last_30_days) AS actives
FROM google_play__country_report
GROUP BY month, region ORDER BY month, region