SELECT 
  u."Age group",
  COUNT(DISTINCT u."User ID") as user_count,
  SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) as at_risk_count,
  ROUND(100.0 * SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) / COUNT(DISTINCT u."User ID"), 2) as churn_risk_pct,
  ROUND(AVG(m."Number of Shares"), 2) as avg_shares,
  ROUND(AVG(m."Event Feedback Rating"), 2) as avg_feedback_rating,
  ROUND(AVG(m."Event Conversion Rate"), 2) as avg_conversion_rate,
  ROUND(AVG(m."Event Dwell Time"), 2) as avg_dwell_time
FROM user_basic_information_table_1 u
LEFT JOIN user_tags_table t ON u."User ID" = t."User ID"
LEFT JOIN marketing_campaign_interaction m ON u."User ID" = m."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"