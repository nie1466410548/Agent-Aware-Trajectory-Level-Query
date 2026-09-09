-- Bot ratio buckets vs retention within churn_watch
WITH company_dim AS (
  SELECT DISTINCT company_name
  FROM intercom__company_enhanced
  WHERE all_company_tags LIKE '%segment:churn_watch%'
),
conv_bot AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    COUNT(*) AS total_convs,
    SUM(CASE WHEN ce.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS bot_ratio
  FROM intercom__conversation_enhanced ce
  GROUP BY ce.all_contact_company_names
)
SELECT 
  CASE WHEN cb.bot_ratio <= 0.25 THEN '0-25%'
       WHEN cb.bot_ratio <= 0.50 THEN '25-50%'
       WHEN cb.bot_ratio <= 0.75 THEN '50-75%'
       ELSE '75-100%' END AS bot_ratio_bucket,
  COUNT(*) AS companies,
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention
FROM company_dim cd
JOIN conv_bot cb ON cd.company_name = cb.company_name
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY 1
ORDER BY 1