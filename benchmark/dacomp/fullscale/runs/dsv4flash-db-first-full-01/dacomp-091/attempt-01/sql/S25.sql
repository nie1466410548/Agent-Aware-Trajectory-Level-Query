SELECT
  ROUND(100.0 * (
    SELECT ABS(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)) FROM quickbooks__general_ledger
    WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
  ) / NULLIF(ABS(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)), 0), 2) AS gl_outflow_share_pct
FROM quickbooks__general_ledger
LIMIT 1