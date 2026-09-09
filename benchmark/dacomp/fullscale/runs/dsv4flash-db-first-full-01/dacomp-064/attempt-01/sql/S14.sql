SELECT 
  AVG(engagement_depth_score) AS avg_depth,
  AVG(engagement_breadth_score) AS avg_breadth,
  AVG(issues_reported) AS avg_reported,
  AVG(issues_assigned) AS avg_assigned,
  AVG(total_outbound_influence) AS avg_outbound,
  AVG(total_inbound_influence) AS avg_inbound,
  AVG(strategic_value_score) AS avg_strategic,
  AVG(direct_network_connections) AS avg_connections,
  AVG(total_engagement_score) AS avg_total_score
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3