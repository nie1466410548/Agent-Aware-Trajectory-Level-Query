-- Target stakeholders' issue counts and closest times
SELECT 
  s.stakeholder_id,
  s.user_display_name,
  s.engagement_depth_score,
  s.engagement_breadth_score,
  s.total_outbound_influence,
  s.total_inbound_influence,
  s.issues_assigned,
  s.issues_reported,
  s.engagement_impact_score,
  s.cross_functional_projects,
  s.strategic_value_score,
  s.direct_network_connections,
  s.response_pattern_type,
  s.engagement_risk_status
FROM jira__stakeholder_engagement_insights s
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
ORDER BY s.total_engagement_score DESC
LIMIT 20