SELECT health_grade, COUNT(*) n, 
       ROUND(AVG(overall_health_score),1) avg_health,
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(AVG(completion_percentage),1) avg_comp
FROM asana__project_analytics
GROUP BY health_grade ORDER BY health_grade