WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp, COUNT(*) AS n,
  ROUND(AVG(total_projects),2) AS avg_total_projects,
  ROUND(AVG(enterprise_projects),2) AS avg_ent_proj,
  ROUND(AVG(large_projects),2) AS avg_large_proj,
  ROUND(AVG(medium_projects),2) AS avg_med_proj,
  ROUND(AVG(small_projects),2) AS avg_small_proj,
  ROUND(AVG(unique_team_members),2) AS avg_members,
  ROUND(AVG(avg_tasks_per_member),2) AS avg_tasks_per_member,
  ROUND(AVG(high_workload_members),2) AS avg_high_wl_members,
  ROUND(AVG(avg_tasks_per_assignee_across_projects),2) AS avg_tasks_per_assignee,
  ROUND(AVG(total_team_tasks),2) AS avg_total_tasks,
  ROUND(AVG(avg_estimated_completion_days),2) AS avg_est_days,
  ROUND(AVG(avg_project_velocity),2) AS avg_velocity
FROM grp GROUP BY grp