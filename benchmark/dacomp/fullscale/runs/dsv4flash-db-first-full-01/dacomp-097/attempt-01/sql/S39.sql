-- Check time range for past 6 months
SELECT MIN(conversation_created_at), MAX(conversation_created_at), 
       COUNT(*) as total,
       SUM(CASE WHEN conversation_author_type = 'bot' THEN 1 ELSE 0 END) as bot_convs,
       SUM(CASE WHEN conversation_author_type = 'contact' THEN 1 ELSE 0 END) as contact_convs
FROM intercom__conversation_metrics