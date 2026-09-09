
  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_organization
  FROM la WHERE rn=1
