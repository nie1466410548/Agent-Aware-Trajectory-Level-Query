SELECT 
  influence_level,
  COUNT(*) AS n,
  AVG(direct_network_connections) AS avg_conn,
  MIN(direct_network_connections) AS min_conn,
  MAX(direct_network_connections) AS max_conn,
  AVG(cross_functional_projects) AS avg_cross_func,
  AVG(total_engagement_score) AS avg_engagement
FROM jira__stakeholder_engagement_insights
GROUP BY influence_level
ORDER BY avg_conn DESC