-- Final summary stats
SELECT 
  ROUND(AVG(registration_retention_7d), 4) AS overall_weekly_retention,
  ROUND(AVG(registration_retention_30d), 4) AS overall_monthly_retention,
  ROUND(AVG(contacts_active_7d), 1) AS avg_active_7d,
  ROUND(AVG(contacts_active_30d), 1) AS avg_active_30d,
  ROUND(AVG(total_conversations), 1) AS avg_convs_per_company
FROM intercom__company_metrics