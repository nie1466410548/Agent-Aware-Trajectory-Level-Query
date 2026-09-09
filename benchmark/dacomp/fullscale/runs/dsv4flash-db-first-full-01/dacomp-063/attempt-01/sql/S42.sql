SELECT COUNT(*) as overlap FROM (
  SELECT DISTINCT stakeholder_id FROM jira__stakeholder_engagement_insights
  INTERSECT
  SELECT DISTINCT user_id FROM jira__team_performance_dashboard
)