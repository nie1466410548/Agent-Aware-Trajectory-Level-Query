SELECT management_priority, health_grade, COUNT(*) n, ROUND(AVG(roi_efficiency_ratio),4) avg_roi
FROM asana__project_analytics
GROUP BY management_priority, health_grade
ORDER BY management_priority, health_grade