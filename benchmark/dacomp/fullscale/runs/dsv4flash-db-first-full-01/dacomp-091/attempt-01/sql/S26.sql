SELECT
  ROUND(100.0 * (
    SELECT SUM(avg_monthly_spend) FROM quickbooks__vendor_performance
    WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
  ) / NULLIF(SUM(avg_monthly_spend), 0), 2) AS vp_spend_share_pct
FROM quickbooks__vendor_performance
LIMIT 1