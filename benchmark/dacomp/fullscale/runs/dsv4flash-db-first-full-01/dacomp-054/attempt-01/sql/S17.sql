SELECT COUNT(DISTINCT stripe_customer_id) AS distinct_stripe_value,
       COUNT(DISTINCT zendesk_user_id) AS distinct_zd_value,
       COUNT(DISTINCT primary_email) AS distinct_email_value
FROM customer360__customer_value_analysis