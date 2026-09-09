SELECT customer_id, customer_name, company_name, payment_rate_percentage, outstanding_balance, credit_score, business_stability_score, total_invoices, total_invoice_amount, avg_invoice_amount, customer_lifespan_days, profitability_tier 
FROM quickbooks__customer_analytics 
WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
ORDER BY outstanding_balance DESC