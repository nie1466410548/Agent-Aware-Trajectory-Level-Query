SELECT vendor_id, account_type,
  ROUND(SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END),2) AS spend_last12,
  ROUND(SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END),2) AS spend_prior12,
  COUNT(*) AS n_tx,
  COUNT(DISTINCT transaction_date) AS n_active_days
FROM quickbooks__general_ledger
WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
GROUP BY vendor_id, account_type
ORDER BY vendor_id, account_type