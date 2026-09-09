SELECT COUNT(*) as cnt FROM (
  SELECT all_conversation_contacts FROM intercom__conversation_enhanced GROUP BY all_conversation_contacts HAVING COUNT(*)=1
)