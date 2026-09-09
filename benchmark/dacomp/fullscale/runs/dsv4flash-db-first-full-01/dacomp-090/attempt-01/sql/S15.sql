SELECT 
  ROUND(AVG(payment_rate_percentage),2) AS avg_payment_rate_all,
  ROUND(AVG(outstanding_balance),2) AS avg_outstanding_all,
  ROUND(SUM(outstanding_balance),2) AS total_outstanding_all,
  COUNT(*) AS n_all
FROM quickbooks__customer_analytics