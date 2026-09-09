SELECT 
  'High-Risk' AS group_name,
  COUNT(*) AS n,
  ROUND(AVG(customer_lifespan_days), 2) AS avg_lifespan_days,
  ROUND(AVG(total_invoices), 2) AS avg_total_invoices,
  ROUND(AVG(avg_invoice_amount), 2) AS avg_invoice_amount,
  ROUND(AVG(credit_score), 2) AS avg_credit_score,
  ROUND(AVG(business_stability_score), 2) AS avg_stability,
  ROUND(AVG(outstanding_balance), 2) AS avg_outstanding,
  ROUND(AVG(payment_rate_percentage), 2) AS avg_payment_rate,
  ROUND(AVG(active_months), 2) AS avg_active_months,
  ROUND(AVG(customer_lifespan_days), 2) AS avg_lifespan
FROM quickbooks__customer_analytics 
WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
UNION ALL
SELECT 
  'Normal' AS group_name,
  COUNT(*) AS n,
  ROUND(AVG(customer_lifespan_days), 2) AS avg_lifespan_days,
  ROUND(AVG(total_invoices), 2) AS avg_total_invoices,
  ROUND(AVG(avg_invoice_amount), 2) AS avg_invoice_amount,
  ROUND(AVG(credit_score), 2) AS avg_credit_score,
  ROUND(AVG(business_stability_score), 2) AS avg_stability,
  ROUND(AVG(outstanding_balance), 2) AS avg_outstanding,
  ROUND(AVG(payment_rate_percentage), 2) AS avg_payment_rate,
  ROUND(AVG(active_months), 2) AS avg_active_months,
  ROUND(AVG(customer_lifespan_days), 2) AS avg_lifespan
FROM quickbooks__customer_analytics 
WHERE NOT (payment_rate_percentage < 75 AND outstanding_balance > 15000)