
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
)
SELECT customer_id, STRFTIME('%Y-%m', transaction_date) AS month, SUM(gross_profit) AS monthly_gp
FROM quickbooks__profitability_analysis
WHERE transaction_date >= (SELECT cutoff_date FROM date_range)
GROUP BY customer_id, STRFTIME('%Y-%m', transaction_date)
