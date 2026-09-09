WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp, ROUND(AVG(overdue_team_tasks*100.0/total_team_tasks),1) AS pct_overdue_tasks,
  ROUND(AVG(active_team_tasks*100.0/total_team_tasks),1) AS pct_active_tasks,
  ROUND(AVG(completed_team_tasks*100.0/total_team_tasks),1) AS pct_completed_tasks,
  ROUND(AVG(overdue_projects*100.0/total_projects),1) AS pct_overdue_projects
FROM grp GROUP BY grp