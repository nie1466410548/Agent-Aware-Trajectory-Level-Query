SELECT calendar_date, account_sub_type, SUM(amount) AS amount
FROM quickbooks__balance_sheet
WHERE account_type = 'Accounts Receivable'
  AND calendar_date = (SELECT MAX(calendar_date) FROM quickbooks__balance_sheet WHERE account_type = 'Accounts Receivable')
GROUP BY calendar_date, account_sub_type
ORDER BY account_sub_type