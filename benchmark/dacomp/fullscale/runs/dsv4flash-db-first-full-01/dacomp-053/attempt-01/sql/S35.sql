WITH grp AS (
  SELECT *,
    CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
         WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
         ELSE 'Other' END AS grp
  FROM asana__project_analytics
)
SELECT grp, COUNT(*) n,
  ROUND(100.0*SUM(CASE WHEN team_size_category='small_team' THEN 1 ELSE 0 END)/COUNT(*),1) pct_small_team,
  ROUND(100.0*SUM(CASE WHEN team_size_category='medium_team' THEN 1 ELSE 0 END)/COUNT(*),1) pct_medium_team,
  ROUND(100.0*SUM(CASE WHEN team_size_category='large_team' THEN 1 ELSE 0 END)/COUNT(*),1) pct_large_team,
  ROUND(100.0*SUM(CASE WHEN project_size_category='small' THEN 1 ELSE 0 END)/COUNT(*),1) pct_small_proj,
  ROUND(100.0*SUM(CASE WHEN project_size_category='medium' THEN 1 ELSE 0 END)/COUNT(*),1) pct_medium_proj,
  ROUND(100.0*SUM(CASE WHEN project_size_category='large' THEN 1 ELSE 0 END)/COUNT(*),1) pct_large_proj,
  ROUND(100.0*SUM(CASE WHEN management_priority='high' THEN 1 ELSE 0 END)/COUNT(*),1) pct_high_priority,
  ROUND(100.0*SUM(CASE WHEN management_priority='medium' THEN 1 ELSE 0 END)/COUNT(*),1) pct_medium_priority,
  ROUND(100.0*SUM(CASE WHEN management_priority='low' THEN 1 ELSE 0 END)/COUNT(*),1) pct_low_priority,
  ROUND(100.0*SUM(CASE WHEN project_maturity_phase='execution' THEN 1 ELSE 0 END)/COUNT(*),1) pct_execution,
  ROUND(100.0*SUM(CASE WHEN risk_level='minimal_risk' THEN 1 ELSE 0 END)/COUNT(*),1) pct_minimal_risk,
  ROUND(100.0*SUM(CASE WHEN risk_level='low_risk' THEN 1 ELSE 0 END)/COUNT(*),1) pct_low_risk,
  ROUND(100.0*SUM(CASE WHEN risk_level='medium_risk' THEN 1 ELSE 0 END)/COUNT(*),1) pct_medium_risk,
  ROUND(100.0*SUM(CASE WHEN risk_level='high_risk' THEN 1 ELSE 0 END)/COUNT(*),1) pct_high_risk
FROM grp
GROUP BY grp ORDER BY grp