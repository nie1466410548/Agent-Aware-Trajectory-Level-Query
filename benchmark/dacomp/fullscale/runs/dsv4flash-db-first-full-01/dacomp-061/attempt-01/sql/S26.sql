SELECT project_name,
  COUNT(*) as team_size,
  SUM(at_churn_risk) as churn_risk_count,
  SUM(inactive_recently) as inactive_count,
  AVG(consistency_percentage) as avg_consistency,
  AVG(resolution_rate_percentage) as avg_resolution_rate,
  AVG(overall_performance_score) as avg_performance,
  AVG(avg_sprint_completion_rate) as avg_sprint_completion,
  AVG(days_since_first_issue) as avg_tenure_days,
  AVG(estimate_accuracy_percentage) as avg_estimate_accuracy
FROM jira__team_performance_dashboard
GROUP BY project_name