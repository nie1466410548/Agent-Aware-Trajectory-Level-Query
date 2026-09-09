
  SELECT customer_id, customer_lifespan_days, total_invoices, avg_invoice_amount,
         credit_score, business_stability_score, outstanding_balance, payment_rate_percentage,
         overdue_count_12m, avg_payment_days_12m, days_since_last_invoice, revenue_growth_rate_12m,
         active_months, total_invoice_amount, monthly_revenue_avg, payment_timeliness_score,
         total_payments, unique_products_purchased, revenue_growth_yoy_pct,
         CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
