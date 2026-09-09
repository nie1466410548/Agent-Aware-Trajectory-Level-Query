-- Check first_response:bot/human tag distribution
SELECT 
  CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 'bot' ELSE 'human' END as responder_type,
  COUNT(*) as cnt
FROM intercom__conversation_enhanced
GROUP BY CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 'bot' ELSE 'human' END