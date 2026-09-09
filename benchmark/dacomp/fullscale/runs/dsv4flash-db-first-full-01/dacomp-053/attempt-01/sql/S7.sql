SELECT health_grade,
       COUNT(*) AS n_projects,
       ROUND(AVG(roi_efficiency_ratio),4) AS avg_roi,
       ROUND(AVG(completion_percentage),2) AS avg_completion,
       ROUND(100.0*SUM(CASE WHEN elapsed_days > planned_duration_days*1.2 THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_exceed_duration_20pct
FROM asana__project_analytics
GROUP BY health_grade
ORDER BY health_grade