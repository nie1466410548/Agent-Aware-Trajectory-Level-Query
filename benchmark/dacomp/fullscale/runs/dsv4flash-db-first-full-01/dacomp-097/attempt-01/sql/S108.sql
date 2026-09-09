-- Conversation volume per company vs retention within churn_watch
WITH company_dim AS (
  SELECT DISTINCT company_name
  FROM intercom__company_enhanced
  WHERE all_company_tags LIKE '%segment:churn_watch%'
),
conv_counts AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    COUNT(*) AS total_convs
  FROM intercom__conversation_enhanced ce
  GROUP BY ce.all_contact_company_names
)
SELECT 
  CASE WHEN cc.total_convs <= 1 THEN '0-1'
       WHEN cc.total_convs <= 3 THEN '2-3'
       WHEN cc.total_convs <= 5 THEN '4-5'
       ELSE '6+' END AS conv_volume_bucket,
  COUNT(*) AS companies,
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention
FROM company_dim cd
JOIN conv_counts cc ON cd.company_name = cc.company_name
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY 1
ORDER BY 1