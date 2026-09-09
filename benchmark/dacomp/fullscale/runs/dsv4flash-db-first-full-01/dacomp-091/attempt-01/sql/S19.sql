SELECT
  ROUND(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END),2) AS total_outflow_all,
  ROUND(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)/24.0,2) AS avg_monthly_outflow_all_gl,
  ROUND(SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END),2) AS total_outflow_selected,
  ROUND(SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END)/24.0,2) AS avg_monthly_outflow_selected_gl,
  ROUND(SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END),2) AS total_inflow_all
FROM quickbooks__general_ledger