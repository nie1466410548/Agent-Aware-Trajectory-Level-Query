-- Weekly retention: contacts with is_active_7d=1 and retained_7d=1 at company level
WITH company_weekly AS (
  SELECT 
    all_contact_company_names AS company_name,
    MAX(CASE WHEN is_active_7d = 1 THEN 1 ELSE 0 END) AS has_active,
    MAX(CASE WHEN retained_7d = 1 THEN 1 ELSE 0 END) AS has_retained
  FROM intercom__contact_enhanced
  GROUP BY all_contact_company_names
)
SELECT 
  COUNT(*) AS total_companies,
  SUM(has_active) AS active_companies,
  SUM(has_retained) AS retained_companies,
  ROUND(100.0 * SUM(has_retained) / NULLIF(SUM(has_active), 0), 2) AS weekly_retention_pct
FROM company_weekly