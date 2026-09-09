-- Verify response delay interpretation: first_admin_response_at - conversation_created_at
SELECT 
  conversation_id,
  conversation_created_at,
  first_admin_response_at,
  time_to_first_response_minutes,
  ROUND((julianday(first_admin_response_at) - julianday(conversation_created_at)) * 1440, 2) AS computed_delay
FROM intercom__conversation_metrics
LIMIT 10