SELECT
  vendor_id,
  account_type,
  ROUND(spend_last12,2) AS spend_last12,
  ROUND(spend_prior12,2) AS spend_prior12,
  ROUND(CASE WHEN ABS(spend_prior12) > 0 THEN (spend_last12 - spend_prior12) / ABS(spend_prior12) * 100 ELSE NULL END, 4) AS spend_change_rate_pct,
  n_tx,
  n_active_days,
  ROUND(n_tx * 1.0 / NULLIF(n_active_days, 0), 4) AS tx_frequency_density
FROM (
  SELECT vendor_id, account_type,
    SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) AS spend_last12,
    SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) AS spend_prior12,
    COUNT(*) AS n_tx,
    COUNT(DISTINCT transaction_date) AS n_active_days
  FROM quickbooks__general_ledger
  WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
  GROUP BY vendor_id, account_type
) t
ORDER BY vendor_id, account_type