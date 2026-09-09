SELECT conversation_id, conversation_created_at, first_admin_response_at, time_to_first_response_minutes, all_conversation_tags
FROM intercom__conversation_metrics
WHERE conversation_id IN (
  SELECT conversation_id FROM intercom__conversation_enhanced 
  WHERE all_conversation_contacts = 'ffab45627106488abe488ad9'
)
ORDER BY conversation_created_at