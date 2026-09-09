WITH split AS (
  SELECT conversation_id, value as tag FROM intercom__conversation_enhanced, json_each('["' || replace(all_conversation_tags, ', ', '","') || '"]') WHERE all_conversation_tags IS NOT NULL AND all_conversation_tags != ''
)
SELECT tag, COUNT(*) as cnt FROM split GROUP BY tag ORDER BY cnt DESC