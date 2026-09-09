SELECT health_grade,
       SUM(CASE WHEN roi_efficiency_ratio >= 0.5 THEN 1 ELSE 0 END) AS roi_ge_05,
       SUM(CASE WHEN roi_efficiency_ratio >= 0.8 THEN 1 ELSE 0 END) AS roi_ge_08,
       SUM(CASE WHEN roi_efficiency_ratio >= 1.0 THEN 1 ELSE 0 END) AS roi_ge_10
FROM asana__project_analytics GROUP BY health_grade ORDER BY health_grade