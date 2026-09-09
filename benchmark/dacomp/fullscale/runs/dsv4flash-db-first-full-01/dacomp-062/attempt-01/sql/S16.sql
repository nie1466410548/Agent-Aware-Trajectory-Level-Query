SELECT 
  stakeholder_archetype,
  COUNT(*) AS n,
  ROUND(AVG(direct_network_connections),2) AS avg_conn,
  ROUND(AVG(cross_functional_projects),2) AS avg_cross_func,
  ROUND(AVG(total_engagement_score),2) AS avg_engagement,
  ROUND(AVG(engagement_quality_score),2) AS avg_quality,
  ROUND(AVG(engagement_impact_score),2) AS avg_impact
FROM jira__stakeholder_engagement_insights
GROUP BY stakeholder_archetype
ORDER BY avg_conn DESC