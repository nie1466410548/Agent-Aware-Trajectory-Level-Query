WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp, workload_balance_status, COUNT(*) AS n FROM grp GROUP BY grp, workload_balance_status ORDER BY grp, n DESC