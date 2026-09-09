SELECT COUNT(DISTINCT CONCAT(marketo_lead_id, '-', stripe_customer_id, '-', zendesk_user_id)) AS distinct_combo
FROM customer360__customer_activity_metrics