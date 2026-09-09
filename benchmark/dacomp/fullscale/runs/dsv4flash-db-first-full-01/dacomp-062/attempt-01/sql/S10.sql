SELECT 
  total_projects_involved,
  AVG(direct_network_connections) AS avg_connections,
  COUNT(*) AS n_stakeholders
FROM jira__stakeholder_engagement_insights
GROUP BY total_projects_involved
ORDER BY total_projects_involved