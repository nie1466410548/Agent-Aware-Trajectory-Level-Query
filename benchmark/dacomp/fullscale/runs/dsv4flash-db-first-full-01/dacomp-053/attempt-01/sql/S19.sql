SELECT health_grade,
       COUNT(*) n,
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(MIN(roi_efficiency_ratio),4) min_roi,
       ROUND(MAX(roi_efficiency_ratio),4) max_roi,
       ROUND(AVG(overall_health_score),1) avg_health,
       ROUND(AVG(comprehensive_project_score),2) avg_cps,
       ROUND(AVG(efficiency_score),1) avg_eff,
       ROUND(AVG(collaboration_score),1) avg_collab,
       ROUND(AVG(time_management_score),1) avg_time
FROM asana__project_analytics
GROUP BY health_grade ORDER BY health_grade