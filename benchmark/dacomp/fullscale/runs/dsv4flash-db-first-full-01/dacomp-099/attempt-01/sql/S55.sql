
SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type,
       cm.count_total_parts, cm.time_to_first_response_minutes
FROM intercom__conversation_enhanced c
LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
