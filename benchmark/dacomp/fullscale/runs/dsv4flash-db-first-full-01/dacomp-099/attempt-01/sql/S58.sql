
SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type
FROM intercom__conversation_enhanced
WHERE all_contact_company_names = 'Edge Platforms'
