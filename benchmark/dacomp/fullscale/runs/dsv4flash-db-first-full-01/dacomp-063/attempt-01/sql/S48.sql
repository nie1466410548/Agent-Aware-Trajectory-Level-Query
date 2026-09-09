-- Team performance patterns for high performers
SELECT 
  s.engagement_risk_status,
  CASE WHEN t.overall_performance_score > 80 THEN 'High Perf' ELSE 'Low Perf' END as perf_group,
  COUNT(*) as cnt,
  AVG(t.resolution_rate_percentage) as avg_res_rate,
  AVG(t.avg_resolution_days) as avg_res_days,
  AVG(t.estimate_accuracy_percentage) as avg_est_acc,
  AVG(t.consistency_percentage) as avg_consistency,
  AVG(t.unique_collaborators_on_issues) as avg_collaborators,
  AVG(t.at_churn_risk) as avg_churn,
  AVG(t.poor_estimation) as avg_poor_est,
  AVG(t.inactive_recently) as avg_inactive
FROM jira__team_performance_dashboard t
JOIN jira__stakeholder_engagement_insights s ON t.user_id = s.stakeholder_id
GROUP BY s.engagement_risk_status, perf_group
ORDER BY s.engagement_risk_status, perf_group