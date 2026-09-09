SELECT account_type,
  ROUND(SUM(amount),2) AS total_selected,
  ROUND(SUM(CASE WHEN amount<0 THEN amount ELSE 0 END),2) AS outflow_selected,
  ROUND(SUM(CASE WHEN amount>0 THEN amount ELSE 0 END),2) AS inflow_selected,
  COUNT(*) AS n_tx
FROM quickbooks__general_ledger
WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
GROUP BY account_type ORDER BY account_type