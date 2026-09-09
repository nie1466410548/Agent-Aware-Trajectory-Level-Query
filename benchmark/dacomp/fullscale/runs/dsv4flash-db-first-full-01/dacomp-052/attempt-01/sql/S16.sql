WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp,
  ROUND(AVG(project_management_score),2) AS avg_pm,
  ROUND(AVG(quality_management_score),2) AS avg_qm,
  ROUND(AVG(collaboration_efficiency_score),2) AS avg_ce,
  ROUND(AVG(resource_optimization_score),2) AS avg_ro,
  ROUND(AVG(overall_team_efficiency_score),2) AS avg_eff
FROM grp GROUP BY grp