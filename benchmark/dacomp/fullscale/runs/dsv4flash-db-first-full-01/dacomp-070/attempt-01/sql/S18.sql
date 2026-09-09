
SELECT cr.region, dr.device, strftime('%Y-%m', cr.date_day) AS month,
  SUM(cr.store_listing_visitors) AS visitors, SUM(cr.store_listing_acquisitions) AS acquisitions,
  SUM(dr.device_installs) AS installs, SUM(dr.device_uninstalls) AS uninstalls,
  SUM(dr.update_events) AS updates, SUM(dr.active_devices_last_30_days) AS actives,
  AVG(dr.rolling_total_average_rating) AS rating
FROM google_play__country_report cr
JOIN google_play__device_report dr ON cr.date_day = dr.date_day AND cr.package_name = dr.package_name
GROUP BY cr.region, dr.device, month
ORDER BY cr.region, dr.device, month
