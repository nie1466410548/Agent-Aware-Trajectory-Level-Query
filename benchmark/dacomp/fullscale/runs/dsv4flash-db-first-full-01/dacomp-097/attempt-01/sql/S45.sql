-- Check conversation metrics vs enhanced join keys
SELECT COUNT(*) FROM intercom__conversation_metrics cm
LEFT JOIN intercom__conversation_enhanced ce ON cm.conversation_id = ce.conversation_id
WHERE ce.conversation_id IS NULL