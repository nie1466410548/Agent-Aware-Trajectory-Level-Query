-- Recompute dept coverage treating Engineering as IT proxy
WITH key_accounts AS (
  SELECT account_id, account_name, annual_revenue, number_of_employees, total_contacts, 
         industry_normalized, account_size_segment, company_size_category,
         customer_health_score
  FROM salesforce__customer_360_view
  WHERE annual_revenue >= 71234915
),
contact_stats AS (
  SELECT 
    c.account_id,
    COUNT(*) AS actual_contacts,
    SUM(CASE WHEN c.title LIKE '%Chief%' THEN 1 ELSE 0 END) AS chief_count,
    MAX(CASE WHEN c.department = 'Sales' THEN 1 ELSE 0 END) AS has_sales,
    MAX(CASE WHEN c.department = 'Finance' THEN 1 ELSE 0 END) AS has_finance,
    MAX(CASE WHEN c.department = 'Operations' THEN 1 ELSE 0 END) AS has_operations,
    MAX(CASE WHEN c.department IN ('IT','Engineering') THEN 1 ELSE 0 END) AS has_it,
    MAX(CASE WHEN c.department = 'HR' THEN 1 ELSE 0 END) AS has_hr
  FROM salesforce__contact_enhanced c
  WHERE c.account_id IN (SELECT account_id FROM key_accounts)
  GROUP BY c.account_id
)
SELECT 
  ka.account_id, ka.account_name, ka.annual_revenue, ka.number_of_employees, ka.industry_normalized,
  ka.company_size_category, ka.customer_health_score,
  COALESCE(cs.actual_contacts, 0) AS actual_contacts,
  COALESCE(cs.chief_count, 0) AS chief_count,
  COALESCE(cs.has_sales, 0) AS has_sales,
  COALESCE(cs.has_finance, 0) AS has_finance,
  COALESCE(cs.has_operations, 0) AS has_operations,
  COALESCE(cs.has_it, 0) AS has_it,
  COALESCE(cs.has_hr, 0) AS has_hr,
  (COALESCE(cs.has_sales,0)+COALESCE(cs.has_finance,0)+COALESCE(cs.has_operations,0)+COALESCE(cs.has_it,0)+COALESCE(cs.has_hr,0)) AS dept_coverage,
  CASE WHEN ka.number_of_employees IS NOT NULL AND ka.number_of_employees > 0 
       THEN ROUND(1.0 * COALESCE(cs.actual_contacts, 0) / ka.number_of_employees * 1000, 2) 
       ELSE NULL END AS contact_density_ratio,
  CASE WHEN COALESCE(cs.actual_contacts, 0) > 0 
       THEN ROUND(100.0 * COALESCE(cs.chief_count, 0) / COALESCE(cs.actual_contacts, 0), 2) 
       ELSE 0 END AS decision_maker_ratio
FROM key_accounts ka
LEFT JOIN contact_stats cs ON ka.account_id = cs.account_id
ORDER BY ka.annual_revenue DESC