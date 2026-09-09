
SELECT ct.contact_id, ct.all_contact_company_names AS company_name,
       c.company_id, c.industry, c.plan_name, c.plan_id, c.monthly_spend
FROM intercom__contact_enhanced ct
LEFT JOIN intercom__company_enhanced c ON ct.all_contact_company_names = c.company_name
