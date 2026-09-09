SELECT conversation_id, conversation_created_at, conversation_initiated_type, all_conversation_tags, all_contact_company_names
FROM intercom__conversation_enhanced
WHERE all_conversation_contacts IN (
  SELECT all_conversation_contacts FROM intercom__conversation_enhanced GROUP BY all_conversation_contacts HAVING COUNT(*)=3 LIMIT 1
)
ORDER BY conversation_created_at