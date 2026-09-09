SELECT strftime('%Y-%m', date_day) AS month, package_name,
  AVG(quality_score) AS quality, AVG(crash_rate_per_1k) AS crash, AVG(anr_rate_per_1k) AS anr,
  AVG(revenue_per_active_device) AS rpad, AVG(active_devices) AS active, AVG(daily_revenue) AS rev,
  AVG(daily_churn_rate) AS churn, AVG(daily_install_uninstall_ratio) AS iur
FROM google_play__time_series_trends
GROUP BY month, package_name ORDER BY month, package_name