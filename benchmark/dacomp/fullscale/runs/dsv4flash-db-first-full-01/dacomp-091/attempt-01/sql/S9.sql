SELECT MIN(transaction_date) AS min_date, MAX(transaction_date) AS max_date,
  COUNT(DISTINCT transaction_date) AS n_dates,
  COUNT(DISTINCT account_type) AS n_account_types
FROM quickbooks__general_ledger
WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)