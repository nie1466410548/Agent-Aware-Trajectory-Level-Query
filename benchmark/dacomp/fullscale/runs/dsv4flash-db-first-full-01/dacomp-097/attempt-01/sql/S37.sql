-- Check if company names match exactly between contact and company tables
SELECT COUNT(*) FROM intercom__contact_enhanced c
JOIN intercom__company_enhanced co ON c.all_contact_company_names = co.company_name
LIMIT 10