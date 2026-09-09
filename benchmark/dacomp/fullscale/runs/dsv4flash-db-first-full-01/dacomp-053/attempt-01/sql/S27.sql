SELECT schedule_forecast, health_grade, COUNT(*) n, ROUND(AVG(roi_efficiency_ratio),4) avg_roi
FROM asana__project_analytics
GROUP BY schedule_forecast, health_grade
ORDER BY schedule_forecast, health_grade