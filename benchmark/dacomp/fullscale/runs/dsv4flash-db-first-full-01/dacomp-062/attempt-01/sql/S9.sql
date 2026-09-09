SELECT 
  MIN(complexity_risk_score) AS min_crs,
  AVG(complexity_risk_score) AS avg_crs,
  MAX(complexity_risk_score) AS max_crs,
  MEDIAN(complexity_risk_score) AS median_crs,
  STDEV(complexity_risk_score) AS std_crs,
  MIN(success_probability) AS min_sp,
  AVG(success_probability) AS avg_sp,
  MAX(success_probability) AS max_sp,
  MEDIAN(success_probability) AS median_sp,
  STDEV(success_probability) AS std_sp
FROM jira__project_risk_assessment