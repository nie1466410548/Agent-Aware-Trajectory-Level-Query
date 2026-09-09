SELECT COUNT(*) as matching_names FROM (
  SELECT DISTINCT user_display_name FROM jira__stakeholder_engagement_insights
  INTERSECT
  SELECT DISTINCT user_display_name FROM jira__team_performance_dashboard
)