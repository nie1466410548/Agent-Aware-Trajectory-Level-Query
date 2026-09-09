-- Company-level retention metrics from company_metrics
SELECT 
  ROUND(AVG(registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(registration_retention_30d), 4) AS avg_monthly_retention,
  COUNT(*) AS total_companies
FROM intercom__company_metrics