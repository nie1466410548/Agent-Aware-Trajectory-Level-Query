SELECT project_size_category, COUNT(*) n,
       ROUND(AVG(overall_health_score),1) avg_health,
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(AVG(completion_percentage),1) avg_comp,
       ROUND(AVG(efficiency_score),1) avg_eff,
       ROUND(AVG(time_management_score),1) avg_time,
       ROUND(AVG(complexity_factor),2) avg_complexity,
       ROUND(AVG(elapsed_days*1.0/planned_duration_days),2) avg_elapsed_ratio
FROM asana__project_analytics
GROUP BY project_size_category ORDER BY avg_roi DESC