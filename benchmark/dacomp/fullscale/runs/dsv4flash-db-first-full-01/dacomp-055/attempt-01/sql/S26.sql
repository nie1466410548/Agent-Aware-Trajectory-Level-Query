SELECT v.primary_email, c.email, c.total_sales_amount
FROM customer360__customer_value_analysis v
JOIN customer360__customer c ON v.primary_email = c.email
WHERE v.marketo_lead_id = 8915
LIMIT 10