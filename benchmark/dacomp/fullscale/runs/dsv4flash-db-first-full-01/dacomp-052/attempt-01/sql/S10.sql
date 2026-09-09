WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp,
  ROUND(AVG(avg_project_health),2) AS avg_health,
  ROUND(AVG(avg_project_performance),2) AS avg_performance,
  ROUND(AVG(avg_completion_rate),2) AS avg_completion,
  ROUND(AVG(avg_quality_rate),2) AS avg_quality,
  ROUND(AVG(avg_risk_percentage),2) AS avg_risk,
  ROUND(AVG(on_schedule_rate_pct),2) AS avg_on_schedule,
  ROUND(AVG(overdue_projects),2) AS avg_overdue_projects,
  ROUND(AVG(overdue_team_tasks),2) AS avg_overdue_tasks,
  ROUND(AVG(active_projects),2) AS avg_active_projects
FROM grp GROUP BY grp