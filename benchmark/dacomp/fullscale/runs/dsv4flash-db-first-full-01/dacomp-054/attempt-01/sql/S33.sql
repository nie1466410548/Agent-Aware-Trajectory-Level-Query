-- Get the latest activity record per email
SELECT primary_email, composite_engagement_score, in_marketo, in_stripe, in_zendesk, 
       zendesk_active, primary_engagement_channel, customer_health_score,
       activity_risk_level, engagement_velocity
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
) WHERE rn = 1
LIMIT 10