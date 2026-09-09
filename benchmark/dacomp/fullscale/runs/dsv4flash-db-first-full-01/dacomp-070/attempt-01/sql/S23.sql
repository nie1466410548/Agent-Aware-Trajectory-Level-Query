
SELECT date_day, device, package_name,
       update_events, active_devices_last_30_days,
       rolling_total_average_rating, device_installs, device_uninstalls
FROM google_play__device_report
ORDER BY device, package_name, date_day
