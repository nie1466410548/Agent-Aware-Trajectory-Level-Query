-- Stakeholder characteristics by engagement risk status
SELECT 
  engagement_risk_status,
  COUNT(*) as cnt,
  AVG(total_engagement_score) as avg_engagement,
  AVG(engagement_breadth_score) as avg_breadth,
  AVG(engagement_depth_score) as avg_depth,
  AVG(engagement_quality_score) as avg_quality,
  AVG(engagement_impact_score) as avg_impact,
  AVG(cross_functional_projects) as avg_cross_func,
  AVG(direct_network_connections) as avg_network,
  AVG(total_outbound_influence) as avg_outbound,
  AVG(total_inbound_influence) as avg_inbound,
  AVG(strategic_value_score) as avg_strategic,
  AVG(total_comments_authored) as avg_comments,
  AVG(issues_assigned) as avg_assigned,
  AVG(issues_reported) as avg_reported
FROM jira__stakeholder_engagement_insights
GROUP BY engagement_risk_status