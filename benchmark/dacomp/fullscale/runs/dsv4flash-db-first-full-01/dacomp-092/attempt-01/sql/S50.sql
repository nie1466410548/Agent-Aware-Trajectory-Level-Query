SELECT account_type, account_sub_type, COUNT(*) AS n, SUM(amount) AS total_amount
FROM quickbooks__balance_sheet
WHERE account_type LIKE '%Receivable%' OR account_sub_type LIKE '%Receivable%' OR account_type LIKE '%Asset%'
GROUP BY account_type, account_sub_type
ORDER BY total_amount DESC
LIMIT 30