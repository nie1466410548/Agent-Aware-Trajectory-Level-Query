SELECT
  -- GL-based outflow share
  ROUND(ABS(SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END))
   / NULLIF(ABS(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)), 0) * 100, 2) AS gl_outflow_share_pct,
  -- Vendor performance based spend share
  ROUND(SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN avg_monthly_spend ELSE 0 END)
   / NULLIF(SUM(avg_monthly_spend), 0) * 100, 2) AS vp_spend_share_pct
FROM quickbooks__general_ledger, quickbooks__vendor_performance
LIMIT 1