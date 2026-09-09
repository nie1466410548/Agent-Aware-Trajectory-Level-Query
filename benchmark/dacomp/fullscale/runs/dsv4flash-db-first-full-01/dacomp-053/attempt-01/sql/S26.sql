-- HHLV candidates: health A/B but roi below median (0.5?)
SELECT project_id, overall_health_score, health_grade, roi_efficiency_ratio,
       team_size_category, project_size_category, complexity_factor,
       collaboration_score, management_priority, efficiency_score,
       schedule_forecast, risk_level, project_maturity_phase,
       completion_percentage, elapsed_days, planned_duration_days,
       time_management_score
FROM asana__project_analytics
WHERE health_grade IN ('A','B') AND roi_efficiency_ratio < 0.4
ORDER BY roi_efficiency_ratio ASC