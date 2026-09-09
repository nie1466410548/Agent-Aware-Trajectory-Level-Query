-- Retention by seat bucket
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
)
SELECT 
  cd.seat_bucket,
  COUNT(*) AS companies,
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.seat_bucket
ORDER BY cd.seat_bucket