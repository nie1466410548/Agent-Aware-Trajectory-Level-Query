SELECT COUNT(*) AS matching_rows
FROM customer360__conversion_funnel_analysis f
INNER JOIN customer360__customer_activity_metrics a ON f.marketo_lead_id = a.marketo_lead_id