
  SELECT account_type,
    AVG(spend_change_rate_pct) as avg_change,
    AVG(tx_frequency_density) as avg_freq,
    SUM(spend_last12) as total_last12,
    SUM(spend_prior12) as total_prior12
  FROM (
    SELECT vendor_id, account_type,
      SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) AS spend_last12,
      SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) AS spend_prior12,
      CASE WHEN ABS(SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) > 0
        THEN (SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) - SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END))
             / ABS(SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) * 100
        ELSE NULL END AS spend_change_rate_pct,
      COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT transaction_date), 0) AS tx_frequency_density
    FROM quickbooks__general_ledger
    WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
    GROUP BY vendor_id, account_type
  ) t
  GROUP BY account_type
  ORDER BY account_type
