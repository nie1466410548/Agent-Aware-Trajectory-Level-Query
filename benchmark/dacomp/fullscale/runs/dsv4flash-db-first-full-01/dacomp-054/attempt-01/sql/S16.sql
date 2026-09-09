SELECT COUNT(DISTINCT stripe_customer_id) AS distinct_stripe_funnel,
       COUNT(DISTINCT zendesk_user_id) AS distinct_zd_funnel,
       COUNT(DISTINCT primary_email) AS distinct_email_funnel
FROM customer360__conversion_funnel_analysis