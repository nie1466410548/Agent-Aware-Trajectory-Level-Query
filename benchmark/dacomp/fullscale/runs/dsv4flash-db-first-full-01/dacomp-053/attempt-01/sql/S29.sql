-- Compare ahead-of-schedule projects by health grade: ROI vs key factors
SELECT health_grade, 
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(AVG(completion_percentage),1) avg_comp,
       ROUND(AVG(complexity_factor),2) avg_complexity,
       ROUND(AVG(collaboration_score),1) avg_collab,
       ROUND(AVG(efficiency_score),1) avg_eff,
       ROUND(AVG(time_management_score),1) avg_time
FROM asana__project_analytics
WHERE schedule_forecast = 'ahead_of_schedule'
GROUP BY health_grade ORDER BY health_grade