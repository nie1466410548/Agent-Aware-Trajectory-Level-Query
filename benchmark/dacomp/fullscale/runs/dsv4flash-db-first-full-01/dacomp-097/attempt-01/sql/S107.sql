-- For churn_watch segment, compare high vs low retention companies
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN 'large'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN 'medium'
         ELSE 'small' END AS size_category
  FROM intercom__company_enhanced
  WHERE all_company_tags LIKE '%segment:churn_watch%'
)
SELECT 
  cd.size_category,
  COUNT(*) AS companies,
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention,
  ROUND(AVG(cm.contacts_active_7d), 1) AS avg_active_7d,
  ROUND(AVG(cm.contacts_active_30d), 1) AS avg_active_30d,
  ROUND(AVG(cm.total_conversations), 1) AS avg_total_convs
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.size_category
ORDER BY cd.size_category