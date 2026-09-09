-- Distinct tag fragments in conversation tags
SELECT all_conversation_tags, COUNT(*) as cnt FROM intercom__conversation_enhanced GROUP BY all_conversation_tags ORDER BY cnt DESC LIMIT 30