
SELECT date_day, package_name, quality_score, crash_rate_per_1k, anr_rate_per_1k,
       revenue_per_active_device, active_devices, daily_churn_rate,
       daily_install_uninstall_ratio, wow_install_growth_rate, 
       daily_revenue, avg_transaction_value,
       ma_7d_quality, ma_30d_quality, ma_7d_churn,
       install_volatility_coefficient, revenue_volatility_coefficient,
       install_trend, revenue_trend, risk_growth_profile, performance_momentum,
       install_stability
FROM google_play__time_series_trends
ORDER BY package_name, date_day
