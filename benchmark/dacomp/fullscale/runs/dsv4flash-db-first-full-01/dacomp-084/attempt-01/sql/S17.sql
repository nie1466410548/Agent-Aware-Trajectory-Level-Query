SELECT organization_size_category,
  ROUND(MIN(organization_health_score),1) min_h,
  ROUND(MAX(organization_health_score),1) max_h,
  ROUND(AVG(organization_health_score),1) mean_h,
  ROUND(MEDIAN(organization_health_score),1) median_h,
  ROUND(STDDEV(organization_health_score),1) sd_h
FROM workday__organization_overview
GROUP BY organization_size_category