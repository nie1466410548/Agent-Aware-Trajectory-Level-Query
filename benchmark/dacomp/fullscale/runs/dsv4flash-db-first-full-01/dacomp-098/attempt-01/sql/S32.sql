SELECT ce.conversation_id, ce.conversation_created_at, ce.conversation_initiated_type, ce.all_conversation_tags,
       cm.first_admin_response_at, cm.time_to_first_response_minutes
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
WHERE ce.all_conversation_contacts = 'ffab45627106488abe488ad9'
ORDER BY ce.conversation_created_at