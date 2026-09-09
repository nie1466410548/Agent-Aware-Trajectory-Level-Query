SELECT risk_group,
  ROUND(MIN(customer_lifespan_days),1) AS min_life, ROUND(MAX(customer_lifespan_days),1) AS max_life,
  ROUND(AVG(customer_lifespan_days),1) AS avg_life,
  ROUND(AVG(total_invoices),2) AS avg_inv_cnt,
  ROUND(AVG(avg_invoice_amount),2) AS avg_inv_amt,
  ROUND(MIN(avg_invoice_amount),2) AS min_inv_amt, ROUND(MAX(avg_invoice_amount),2) AS max_inv_amt,
  ROUND(AVG(overdue_count_12m),2) AS avg_overdue_12m,
  ROUND(AVG(avg_payment_days_12m),2) AS avg_pay_days_12m,
  ROUND(AVG(days_since_last_invoice),1) AS avg_days_since_last,
  ROUND(AVG(revenue_growth_rate_12m),2) AS avg_rev_growth
FROM (
  SELECT customer_id, customer_lifespan_days, total_invoices, avg_invoice_amount, overdue_count_12m, avg_payment_days_12m, days_since_last_invoice, revenue_growth_rate_12m,
    CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
)
GROUP BY risk_group