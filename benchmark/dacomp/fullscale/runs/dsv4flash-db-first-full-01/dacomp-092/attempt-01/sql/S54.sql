-- AR aging trend: past due ratio over time
SELECT 
  calendar_date,
  SUM(CASE WHEN account_sub_type = 'Current (0-30 days)' THEN amount ELSE 0 END) AS current_ar,
  SUM(CASE WHEN account_sub_type != 'Current (0-30 days)' THEN amount ELSE 0 END) AS past_due_ar,
  SUM(amount) AS total_ar,
  ROUND(100.0 * SUM(CASE WHEN account_sub_type != 'Current (0-30 days)' THEN amount ELSE 0 END) / NULLIF(SUM(amount),0), 2) AS past_due_pct
FROM quickbooks__balance_sheet
WHERE account_type = 'Accounts Receivable'
GROUP BY calendar_date
ORDER BY calendar_date