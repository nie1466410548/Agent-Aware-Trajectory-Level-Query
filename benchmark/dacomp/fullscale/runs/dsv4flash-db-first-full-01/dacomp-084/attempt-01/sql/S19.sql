WITH ranked AS (
  SELECT organization_id, organization_size_category, organization_health_score,
    ROW_NUMBER() OVER (PARTITION BY organization_size_category ORDER BY organization_health_score) rn,
    COUNT(*) OVER (PARTITION BY organization_size_category) n
  FROM workday__organization_overview
)
SELECT organization_size_category,
  ROUND(AVG(organization_health_score),2) AS mean,
  ROUND(AVG(CASE WHEN rn*1.0/n <= 0.25 THEN organization_health_score END),2) AS p25,
  ROUND(AVG(CASE WHEN rn*1.0/n <= 0.5 AND rn*1.0/n > 0.25 THEN organization_health_score END),2) AS p50_approx,
  ROUND(AVG(CASE WHEN rn*1.0/n <= 0.75 AND rn*1.0/n > 0.5 THEN organization_health_score END),2) AS p75_approx,
  ROUND(STDDEV(organization_health_score),2) AS sd
FROM ranked
GROUP BY organization_size_category