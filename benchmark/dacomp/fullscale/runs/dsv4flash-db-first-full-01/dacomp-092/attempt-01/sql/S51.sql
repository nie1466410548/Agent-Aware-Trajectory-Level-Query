SELECT account_sub_type, COUNT(DISTINCT calendar_date) AS n_dates, 
       MIN(calendar_date) AS min_date, MAX(calendar_date) AS max_date,
       SUM(amount) AS total_amount,
       SUM(converted_amount) AS total_converted
FROM quickbooks__balance_sheet
WHERE account_type = 'Accounts Receivable'
GROUP BY account_sub_type
ORDER BY total_amount DESC