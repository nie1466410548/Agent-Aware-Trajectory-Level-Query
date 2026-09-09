SELECT
  ROUND(AVG((enterprise_projects+large_projects)*100.0/total_projects),1) AS avg_pct_large_ent,
  MIN((enterprise_projects+large_projects)*100.0/total_projects) AS min_pct_large_ent,
  MAX((enterprise_projects+large_projects)*100.0/total_projects) AS max_pct_large_ent,
  ROUND(AVG(avg_estimated_completion_days),1) AS avg_est_days_target,
  MIN(avg_estimated_completion_days) AS min_days,
  MAX(avg_estimated_completion_days) AS max_days,
  ROUND(AVG(overdue_team_tasks*100.0/total_team_tasks),1) AS avg_pct_overdue_tasks,
  ROUND(AVG(active_team_tasks*100.0/total_team_tasks),1) AS avg_pct_active_tasks,
  ROUND(AVG(completed_team_tasks*100.0/total_team_tasks),1) AS avg_pct_completed_tasks,
  ROUND(AVG(high_workload_members*100.0/unique_team_members),1) AS avg_pct_high_wl
FROM asana__team_efficiency_metrics
WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70