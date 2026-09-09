SELECT health_grade,
       ROUND(MIN(overall_health_score),0) min_h, ROUND(MAX(overall_health_score),0) max_h,
       ROUND(AVG(overall_health_score),1) avg_h
FROM asana__project_analytics GROUP BY health_grade ORDER BY health_grade