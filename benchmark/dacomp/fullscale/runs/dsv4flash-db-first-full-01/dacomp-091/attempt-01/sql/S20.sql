SELECT account_type,
  ROUND(SUM(amount),2) AS total_all,
  ROUND(SUM(CASE WHEN amount<0 THEN amount ELSE 0 END),2) AS outflow_all,
  ROUND(SUM(CASE WHEN amount>0 THEN amount ELSE 0 END),2) AS inflow_all
FROM quickbooks__general_ledger
GROUP BY account_type ORDER BY account_type