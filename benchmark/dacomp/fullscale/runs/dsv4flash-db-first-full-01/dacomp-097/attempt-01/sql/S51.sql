-- Check the conversation enhanced table for last_close_at and first_close_at
SELECT 
  conversation_id, 
  conversation_created_at,
  first_close_at,
  last_close_at,
  first_admin_close_at,
  last_admin_close_at
FROM intercom__conversation_enhanced LIMIT 10