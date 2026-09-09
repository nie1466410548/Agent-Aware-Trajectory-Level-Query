SELECT 
  ROUND(SUM(CASE WHEN roi_efficiency_ratio < 0.1 THEN 1 ELSE 0 END)*100.0/500,1) pct_lt_01,
  ROUND(SUM(CASE WHEN roi_efficiency_ratio < 0.3 THEN 1 ELSE 0 END)*100.0/500,1) pct_lt_03,
  ROUND(SUM(CASE WHEN roi_efficiency_ratio < 0.5 THEN 1 ELSE 0 END)*100.0/500,1) pct_lt_05,
  ROUND(SUM(CASE WHEN roi_efficiency_ratio > 0.8 THEN 1 ELSE 0 END)*100.0/500,1) pct_gt_08,
  ROUND(SUM(CASE WHEN roi_efficiency_ratio > 1.0 THEN 1 ELSE 0 END)*100.0/500,1) pct_gt_10
FROM asana__project_analytics