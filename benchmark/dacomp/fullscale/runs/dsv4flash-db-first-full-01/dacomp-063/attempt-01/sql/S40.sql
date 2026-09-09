SELECT 
  CASE WHEN overall_performance_score > 80 THEN 'perf>80' ELSE 'perf<=80' END as perf_band,
  COUNT(*) as cnt,
  AVG(overall_performance_score) as avg_perf,
  AVG(avg_resolution_days) as avg_res_days,
  AVG(estimate_accuracy_percentage) as avg_est_acc,
  AVG(consistency_percentage) as avg_consistency
FROM jira__team_performance_dashboard
GROUP BY perf_band