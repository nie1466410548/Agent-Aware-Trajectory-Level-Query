SELECT
  c.visitor_id, c.comprehensive_customer_value, c.user_value_score, c.lifecycle_stage,
  c.churn_risk_level, c.engagement_trend, c.feature_adoption_rate
FROM pendo__customer_lifecycle_insights c
JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) vf ON c.visitor_id = vf.visitor_id
LIMIT 10