SELECT
  ROUND(SUM(avg_monthly_spend),2) AS all_vendor_monthly_spend,
  ROUND(SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN avg_monthly_spend ELSE 0 END),2) AS selected_vendor_monthly_spend,
  ROUND(SUM(total_lifetime_spend),2) AS all_lifetime_spend,
  ROUND(SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN total_lifetime_spend ELSE 0 END),2) AS selected_lifetime_spend,
  COUNT(*) AS n_all
FROM quickbooks__vendor_performance