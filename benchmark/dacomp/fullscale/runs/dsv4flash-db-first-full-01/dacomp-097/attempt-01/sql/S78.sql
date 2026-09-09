-- Extract all unique channel values
SELECT DISTINCT 
  SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'channel:'), 
         CASE WHEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'channel:')), '|') > 0 
              THEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'channel:')), '|') - 1 
              ELSE LENGTH(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'channel:'))) END) AS channel_tag
FROM intercom__conversation_enhanced
WHERE all_conversation_tags LIKE '%channel:%'
ORDER BY channel_tag