-- Retention by segment using company_metrics
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
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention,
  ROUND(AVG(cm.contacts_active_7d), 2) AS avg_active_contacts_7d,
  ROUND(AVG(cm.contacts_active_30d), 2) AS avg_active_contacts_30d
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.segment
ORDER BY cd.segment