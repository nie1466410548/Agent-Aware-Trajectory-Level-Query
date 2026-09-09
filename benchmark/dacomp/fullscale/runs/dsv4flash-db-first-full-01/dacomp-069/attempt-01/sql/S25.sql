SELECT region, 
  COUNT(*) AS n_countries,
  ROUND(SUM(avg_daily_revenue),2) AS total_daily_rev,
  ROUND(AVG(avg_daily_revenue),2) AS avg_daily_rev,
  ROUND(AVG(average_revenue_per_user),2) AS avg_arpu,
  ROUND(AVG(avg_transaction_value),2) AS avg_atv,
  ROUND(AVG(app_quality_score),2) AS avg_quality,
  ROUND(AVG(app_crash_rate_per_1k),2) AS avg_crash,
  ROUND(AVG(day_7_retention_rate),3) AS avg_d7_ret,
  ROUND(AVG(day_30_retention_rate),3) AS avg_d30_ret,
  ROUND(AVG(daily_churn_rate),3) AS avg_churn,
  ROUND(AVG(weekly_growth_rate),3) AS avg_growth,
  ROUND(AVG(overall_market_score),2) AS avg_market_score
FROM google_play__geo_market_analysis 
WHERE package_name='com.dev.photoeditor' 
GROUP BY region
ORDER BY total_daily_rev DESC