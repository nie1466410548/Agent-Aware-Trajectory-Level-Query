SELECT DISTINCT 
  CASE WHEN instr(all_conversation_tags,'region:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'region:')+7, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'region:')+7),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'region:')+7),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'region:')+7)) END)
  END AS region,
  COUNT(*) AS cnt
FROM intercom__conversation_enhanced
GROUP BY region ORDER BY cnt DESC