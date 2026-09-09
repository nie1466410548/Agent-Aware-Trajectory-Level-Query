SELECT 
  CASE 
    WHEN direct_network_connections <= 5 THEN 'low_(<=5)'
    WHEN direct_network_connections <= 20 THEN 'mid_(6-20)'
    ELSE 'high_(>20)'
  END AS conn_group,
  engagement_risk_status,
  COUNT(*) AS n,
  ROUND(AVG(total_engagement_score),2) AS avg_engagement
FROM jira__stakeholder_engagement_insights
GROUP BY conn_group, engagement_risk_status
ORDER BY conn_group, engagement_risk_status