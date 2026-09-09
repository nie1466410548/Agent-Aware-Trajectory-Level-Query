SELECT account_type, COUNT(*) AS n_tx, ROUND(SUM(amount),2) AS total_amt, MIN(transaction_date) AS min_d, MAX(transaction_date) AS max_d
FROM quickbooks__general_ledger
WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
GROUP BY account_type
ORDER BY total_amt DESC