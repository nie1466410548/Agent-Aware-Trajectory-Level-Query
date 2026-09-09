
SELECT COUNT(*) as total,
       SUM(CASE WHEN c.company_id IS NOT NULL THEN 1 ELSE 0 END) as matched
FROM (
  SELECT DISTINCT all_contact_company_names as company_name
  FROM intercom__contact_enhanced
) ct
LEFT JOIN intercom__company_enhanced c ON ct.company_name = c.company_name
