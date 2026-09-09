SELECT team_name, team_size_category, workload_balance_status, team_maturity_level, efficiency_grade,
  total_projects, enterprise_projects, large_projects, medium_projects, small_projects,
  avg_completion_rate, avg_project_health, avg_project_performance, avg_quality_rate,
  unique_team_members, avg_tasks_per_member, high_workload_members, high_risk_members,
  avg_estimated_completion_days, on_schedule_rate_pct, avg_risk_percentage,
  overdue_projects, overdue_team_tasks, total_team_tasks, completed_team_tasks,
  overall_team_efficiency_score, improvement_recommendations, team_strengths
FROM asana__team_efficiency_metrics
WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
ORDER BY avg_completion_rate DESC