-- Find projects with abnormally high roi for their health (LHHV candidates)
SELECT project_id, overall_health_score, health_grade, roi_efficiency_ratio,
       team_size_category, project_size_category, complexity_factor,
       collaboration_score, management_priority, efficiency_score,
       schedule_forecast, risk_level, project_maturity_phase,
       completion_percentage, elapsed_days, planned_duration_days,
       time_management_score
FROM asana__project_analytics
WHERE (health_grade IN ('D','F') AND roi_efficiency_ratio > 0.5)
   OR (health_grade = 'D' AND roi_efficiency_ratio > 0.3)
ORDER BY roi_efficiency_ratio DESC