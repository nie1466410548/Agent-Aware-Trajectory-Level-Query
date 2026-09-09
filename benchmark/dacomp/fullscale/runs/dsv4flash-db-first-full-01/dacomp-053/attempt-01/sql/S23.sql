SELECT project_id, overall_health_score, health_grade, roi_efficiency_ratio, completion_percentage, planned_duration_days, elapsed_days
FROM asana__project_analytics
WHERE roi_efficiency_ratio >= 0.8
ORDER BY roi_efficiency_ratio DESC
LIMIT 30