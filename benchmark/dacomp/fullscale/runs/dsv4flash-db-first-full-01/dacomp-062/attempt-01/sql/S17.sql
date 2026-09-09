SELECT 
  response_pattern_type,
  COUNT(*) AS n,
  ROUND(AVG(direct_network_connections),2) AS avg_conn,
  ROUND(AVG(total_engagement_score),2) AS avg_engagement,
  ROUND(AVG(engagement_quality_score),2) AS avg_quality,
  ROUND(AVG(avg_outbound_influence_strength),3) AS avg_influence_strength
FROM jira__stakeholder_engagement_insights
GROUP BY response_pattern_type
ORDER BY avg_conn DESC