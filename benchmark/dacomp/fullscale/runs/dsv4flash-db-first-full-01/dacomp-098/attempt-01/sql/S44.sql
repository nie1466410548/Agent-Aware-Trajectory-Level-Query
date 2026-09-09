
SELECT DISTINCT ct.all_contact_company_names, c.company_id, c.industry, c.plan_name
FROM intercom__contact_enhanced ct
LEFT JOIN intercom__company_enhanced c ON ct.all_contact_company_names = c.company_name
LIMIT 20
