SELECT COUNT(DISTINCT stripe_customer_id) AS distinct_stripe_activity,
       COUNT(DISTINCT zendesk_user_id) AS distinct_zd_activity,
       COUNT(DISTINCT primary_email) AS distinct_email_activity
FROM customer360__customer_activity_metrics