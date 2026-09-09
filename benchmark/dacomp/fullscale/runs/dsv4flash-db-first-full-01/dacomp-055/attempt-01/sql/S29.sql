SELECT COUNT(*) AS total, COUNT(DISTINCT marketo_lead_id || '|' || stripe_customer_id || '|' || zendesk_user_id) AS distinct_key_triple,
COUNT(DISTINCT stripe_customer_id) AS distinct_stripe,
COUNT(DISTINCT primary_email) AS distinct_email
FROM customer360__customer_value_analysis