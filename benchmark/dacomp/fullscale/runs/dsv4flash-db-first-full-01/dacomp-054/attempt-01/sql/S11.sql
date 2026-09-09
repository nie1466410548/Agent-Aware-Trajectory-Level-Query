SELECT COUNT(*) AS matching_rows
FROM customer360__conversion_funnel_analysis f
INNER JOIN customer360__customer_value_analysis v ON f.marketo_lead_id = v.marketo_lead_id