WITH target AS (
  SELECT * FROM asana__team_efficiency_metrics
  WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
)
SELECT
  ROUND(AVG(efficiency_rank),1) AS avg_eff_rank,
  ROUND(AVG(performance_rank),1) AS avg_perf_rank,
  ROUND(AVG(schedule_reliability_rank),1) AS avg_sched_rank,
  ROUND(AVG(quality_rank),1) AS avg_quality_rank,
  ROUND(AVG(project_management_score),1) AS avg_pm_score,
  ROUND(AVG(quality_management_score),1) AS avg_qm_score,
  ROUND(AVG(avg_member_quality_rate),1) AS avg_member_quality
FROM target