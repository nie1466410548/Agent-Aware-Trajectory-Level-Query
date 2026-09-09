-- Distribution of company-level retention
SELECT 
  ROUND(registration_retention_7d, 2) AS ret_7d,
  ROUND(registration_retention_30d, 2) AS ret_30d,
  COUNT(*) AS cnt
FROM intercom__company_metrics
GROUP BY ROUND(registration_retention_7d, 2), ROUND(registration_retention_30d, 2)
ORDER BY ret_7d, ret_30d
LIMIT 20