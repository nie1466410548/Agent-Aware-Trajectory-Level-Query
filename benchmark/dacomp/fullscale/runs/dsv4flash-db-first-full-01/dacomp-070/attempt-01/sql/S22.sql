
SELECT date_day, country_short, region, package_name,
       update_events, active_devices_last_30_days, 
       rolling_total_average_rating, device_installs, net_device_installs
FROM google_play__country_report
ORDER BY region, package_name, date_day
