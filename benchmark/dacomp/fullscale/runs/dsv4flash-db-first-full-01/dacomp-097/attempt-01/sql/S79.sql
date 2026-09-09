-- Extract all unique SLA values
SELECT DISTINCT 
  SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'sla:'), 
         CASE WHEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'sla:')), '|') > 0 
              THEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'sla:')), '|') - 1 
              ELSE LENGTH(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'sla:'))) END) AS sla_tag
FROM intercom__conversation_enhanced
WHERE all_conversation_tags LIKE '%sla:%'
ORDER BY sla_tag