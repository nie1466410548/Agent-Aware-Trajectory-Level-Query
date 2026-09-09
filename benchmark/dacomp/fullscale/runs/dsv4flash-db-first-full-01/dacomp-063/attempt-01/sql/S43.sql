SELECT COUNT(*) as overlap2 FROM (
  SELECT DISTINCT user_id FROM jira__team_performance_dashboard
  INTERSECT
  SELECT DISTINCT stakeholder_id FROM jira__stakeholder_engagement_insights
)