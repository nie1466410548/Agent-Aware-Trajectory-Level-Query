
SELECT strftime('%Y-%m', date_day) AS month, package_name,
  AVG(quality_score) AS quality, AVG(crash_rate_per_1k) AS crash, AVG(anr_rate_per_1k) AS anr,
  AVG(revenue_per_active_device) AS rpad, AVG(active_devices) AS active,
  AVG(ma_7d_quality) AS ma7q, AVG(ma_30d_quality) AS ma30q,
  AVG(wow_install_growth_rate) AS wow_inst, AVG(wow_revenue_growth_rate) AS wow_rev,
  AVG(install_volatility_coefficient) AS inst_vol, AVG(revenue_volatility_coefficient) AS rev_vol
FROM google_play__time_series_trends
GROUP BY month, package_name
ORDER BY package_name, month
