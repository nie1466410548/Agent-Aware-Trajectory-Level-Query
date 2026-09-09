SELECT DISTINCT 
  CASE WHEN instr(all_conversation_tags,'intent:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'intent:')+7, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'intent:')+7),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'intent:')+7),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'intent:')+7)) END)
  END AS intent,
  COUNT(*) AS cnt
FROM intercom__conversation_enhanced
GROUP BY intent ORDER BY cnt DESC