
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
)
SELECT 
  cd.arr_bucket,
  AVG(cm.registration_retention_7d) AS weekly_retention,
  AVG(cm.registration_retention_30d) AS monthly_retention,
  AVG(cm.contacts_active_7d) AS avg_active_7d,
  AVG(cm.contacts_active_30d) AS avg_active_30d
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.arr_bucket
ORDER BY cd.arr_bucket
