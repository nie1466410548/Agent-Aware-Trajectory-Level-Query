
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
)
SELECT 
  cd.segment,
  COUNT(*) AS companies,
  AVG(cm.registration_retention_7d) AS weekly_retention,
  AVG(cm.registration_retention_30d) AS monthly_retention
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.segment
ORDER BY cd.segment
