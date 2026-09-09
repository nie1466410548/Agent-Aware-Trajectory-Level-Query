SELECT management_priority, COUNT(*) n,
       ROUND(AVG(overall_health_score),1) avg_health,
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(AVG(completion_percentage),1) avg_comp,
       ROUND(AVG(elapsed_days*1.0/planned_duration_days),2) avg_elapsed_ratio,
       ROUND(AVG(complexity_factor),2) avg_complexity,
       ROUND(AVG(time_management_score),1) avg_time
FROM asana__project_analytics
GROUP BY management_priority ORDER BY management_priority