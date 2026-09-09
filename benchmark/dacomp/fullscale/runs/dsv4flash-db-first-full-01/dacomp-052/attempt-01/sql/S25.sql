WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp,
  ROUND(AVG(efficiency_rank),1) AS avg_eff_rank,
  ROUND(AVG(performance_rank),1) AS avg_perf_rank,
  ROUND(AVG(schedule_reliability_rank),1) AS avg_sched_rank,
  ROUND(AVG(quality_rank),1) AS avg_quality_rank,
  ROUND(AVG(project_management_score),1) AS avg_pm,
  ROUND(AVG(quality_management_score),1) AS avg_qm
FROM grp GROUP BY grp