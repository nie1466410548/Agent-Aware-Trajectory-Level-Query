SELECT project_id, project_name, health_grade, overall_health_score, roi_efficiency_ratio,
       completion_percentage, efficiency_score, time_management_score, collaboration_score,
       schedule_forecast, risk_level, management_priority, complexity_factor,
       team_size_category, project_size_category, elapsed_days, planned_duration_days,
       focus_areas, success_factors, improvement_opportunities
FROM asana__project_analytics
WHERE (health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3)
ORDER BY roi_efficiency_ratio DESC