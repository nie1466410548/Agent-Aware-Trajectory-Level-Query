WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp,
  ROUND(AVG(top_performers),2) AS avg_top,
  ROUND(AVG(high_performers),2) AS avg_high,
  ROUND(AVG(solid_performers),2) AS avg_solid,
  ROUND(AVG(developing_performers),2) AS avg_dev,
  ROUND(AVG(underperformers),2) AS avg_under,
  ROUND(AVG(high_risk_members),2) AS avg_high_risk,
  ROUND(AVG(avg_member_performance),2) AS avg_member_perf,
  ROUND(AVG(avg_member_completion_rate),2) AS avg_member_cr,
  ROUND(AVG(avg_member_quality_rate),2) AS avg_member_qr,
  ROUND(SUM(high_workload_members)*100.0/SUM(unique_team_members),2) AS pct_high_wl,
  ROUND(SUM(high_risk_members)*100.0/SUM(unique_team_members),2) AS pct_high_risk
FROM grp GROUP BY grp