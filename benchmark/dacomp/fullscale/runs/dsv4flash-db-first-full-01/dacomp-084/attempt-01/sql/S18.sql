WITH t AS (
  SELECT organization_id, organization_size_category, organization_health_score,
    COUNT(*) OVER (PARTITION BY organization_size_category) AS tier_n
  FROM workday__organization_overview
)
SELECT organization_size_category, tier_n,
  ROUND(AVG(organization_health_score),1) mean_h,
  ROUND(MIN(organization_health_score),1) min_h,
  ROUND(MAX(organization_health_score),1) max_h,
  ROUND(AVG(CASE WHEN organization_health_score <= (SELECT MIN(organization_health_score) FROM workday__organization_overview o2 WHERE o2.organization_size_category=t.organization_size_category) THEN organization_health_score END),1) dummy,
  ROUND(AVG(organization_health_score) OVER (),1) overall
FROM t
GROUP BY organization_size_category