SELECT country, region, avg_daily_installs, avg_active_devices, store_visitors_30d, store_installs_30d, avg_daily_revenue,
  ROUND(avg_daily_revenue/avg_daily_installs,2) AS rev_per_install_day,
  ROUND(revenue_last_30_days/store_installs_30d,2) AS rev_per_install_ltv,
  ROUND(avg_daily_revenue*30/store_visitors_30d,2) AS rev_per_visitor,
  ROUND(avg_daily_revenue/avg_active_devices,2) AS rev_per_active_device
FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor' ORDER BY avg_daily_revenue DESC