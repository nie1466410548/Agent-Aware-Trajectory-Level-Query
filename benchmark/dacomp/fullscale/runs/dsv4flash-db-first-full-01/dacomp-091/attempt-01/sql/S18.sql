SELECT
  ROUND(SUM(avg_monthly_spend),2) AS sum_avg_monthly_spend_selected,
  ROUND(SUM(avg_transaction_size),2) AS sum_avg_tx_size,
  ROUND(AVG(avg_monthly_spend),2) AS avg_monthly_spend_per_vendor
FROM quickbooks__vendor_performance
WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7