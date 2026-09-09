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
  ROUND(AVG(overall_health_score),1) avg_health,
  ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
  ROUND(AVG(completion_percentage),1) avg_comp,
  ROUND(AVG(efficiency_score),1) avg_eff,
  ROUND(AVG(time_management_score),1) avg_time,
  ROUND(AVG(collaboration_score),1) avg_collab,
  ROUND(AVG(complexity_factor),2) avg_complexity,
  ROUND(AVG(elapsed_days*1.0/planned_duration_days),2) avg_elapsed_ratio,
  ROUND(100.0*SUM(CASE WHEN schedule_forecast='ahead_of_schedule' THEN 1 ELSE 0 END)/COUNT(*),1) pct_ahead,
  ROUND(100.0*SUM(CASE WHEN schedule_forecast='behind_schedule' THEN 1 ELSE 0 END)/COUNT(*),1) pct_behind,
  ROUND(100.0*SUM(CASE WHEN management_priority='low' THEN 1 ELSE 0 END)/COUNT(*),1) pct_low_priority,
  ROUND(100.0*SUM(CASE WHEN risk_level='minimal_risk' THEN 1 ELSE 0 END)/COUNT(*),1) pct_minimal_risk
FROM grp
GROUP BY grp ORDER BY grp