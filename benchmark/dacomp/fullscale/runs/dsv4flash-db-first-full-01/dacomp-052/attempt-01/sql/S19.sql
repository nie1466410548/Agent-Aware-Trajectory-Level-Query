WITH target AS (
  SELECT * FROM asana__team_efficiency_metrics
  WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
)
SELECT
  SUM(CASE WHEN (enterprise_projects+large_projects)*100.0/total_projects >= 50 THEN 1 ELSE 0 END) AS teams_ge50pct_large,
  SUM(CASE WHEN avg_estimated_completion_days >= 75 THEN 1 ELSE 0 END) AS teams_ge75_days,
  SUM(CASE WHEN high_workload_members*100.0/unique_team_members >= 50 THEN 1 ELSE 0 END) AS teams_ge50pct_high_wl,
  SUM(CASE WHEN avg_risk_percentage >= 30 THEN 1 ELSE 0 END) AS teams_ge30_risk,
  SUM(CASE WHEN on_schedule_rate_pct < 50 THEN 1 ELSE 0 END) AS teams_low_schedule,
  COUNT(*) AS n
FROM target