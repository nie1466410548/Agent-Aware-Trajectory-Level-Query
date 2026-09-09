
SELECT ce.all_conversation_contacts AS contact_id, 
       ce.conversation_initiated_type,
       c.industry,
       c.plan_name
FROM intercom__conversation_enhanced ce
LEFT JOIN intercom__contact_enhanced ct ON ce.all_conversation_contacts = ct.contact_id
LEFT JOIN intercom__company_enhanced c ON ct.all_contact_company_names = c.company_name
LIMIT 10
