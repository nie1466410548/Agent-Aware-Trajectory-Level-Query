-- Extract all unique topic values from tags
SELECT DISTINCT 
  SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'topic:'), 
         CASE WHEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'topic:')), '|') > 0 
              THEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'topic:')), '|') - 1 
              ELSE LENGTH(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'topic:'))) END) AS topic_tag
FROM intercom__conversation_enhanced
WHERE all_conversation_tags LIKE '%topic:%'
ORDER BY topic_tag