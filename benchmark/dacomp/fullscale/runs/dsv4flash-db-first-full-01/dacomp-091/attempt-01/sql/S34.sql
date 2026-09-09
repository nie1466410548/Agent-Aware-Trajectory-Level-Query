SELECT
  account_type,
  COUNT(*) AS n_pairs,
  ROUND(AVG(spend_change_rate_pct),4) AS avg_change_pct,
  ROUND(MEDIAN(spend_change_rate_pct),4) AS median_change_pct,
  ROUND(MIN(spend_change_rate_pct),4) AS min_change_pct,
  ROUND(MAX(spend_change_rate_pct),4) AS max_change_pct,
  ROUND(AVG(tx_frequency_density),4) AS avg_tx_freq_density,
  ROUND(MEDIAN(tx_frequency_density),4) AS median_tx_freq_density,
  ROUND(SUM(spend_last12),2) AS total_vol_last12,
  ROUND(SUM(spend_prior12),2) AS total_vol_prior12
FROM (
  SELECT vendor_id, account_type,
    SUM(ABS(amount)) AS spend_last12,
    SUM(ABS(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) AS spend_prior12,
    CASE WHEN SUM(ABS(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) > 0
      THEN (SUM(CASE WHEN transaction_date >= '2024-10-15' THEN ABS(amount) ELSE 0 END)
           - SUM(CASE WHEN transaction_date < '2024-10-15' THEN ABS(amount) ELSE 0 END))
           / SUM(CASE WHEN transaction_date < '2024-10-15' THEN ABS(amount) ELSE 0 END) * 100
      ELSE NULL END AS spend_change_rate_pct,
    COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT transaction_date), 0) AS tx_frequency_density
  FROM quickbooks__general_ledger
  WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
  GROUP BY vendor_id, account_type
) t
GROUP BY account_type
ORDER BY account_type