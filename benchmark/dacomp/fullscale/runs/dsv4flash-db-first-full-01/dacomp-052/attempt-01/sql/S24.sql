WITH target AS (
  SELECT team_id, team_name, avg_completion_rate,
    avg_project_health, avg_quality_rate, on_schedule_rate_pct,
    avg_estimated_completion_days, (enterprise_projects+large_projects)*100.0/total_projects AS pct_large_ent,
    high_workload_members*100.0/unique_team_members AS pct_high_wl,
    RANK() OVER (ORDER BY avg_completion_rate ASC) AS low_completion_rank
  FROM asana__team_efficiency_metrics
  WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
)
SELECT * FROM target ORDER BY avg_completion_rate ASC LIMIT 10