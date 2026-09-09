-- Overall AR aging structure (all snapshots)
SELECT 
  account_sub_type,
  SUM(amount) AS total_amount,
  ROUND(100.0 * SUM(amount) / SUM(SUM(amount)) OVER (), 2) AS pct_of_total
FROM quickbooks__balance_sheet
WHERE account_type = 'Accounts Receivable'
GROUP BY account_sub_type
ORDER BY total_amount DESC