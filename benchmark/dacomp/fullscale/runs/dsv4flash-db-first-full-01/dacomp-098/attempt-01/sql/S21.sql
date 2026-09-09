SELECT DISTINCT 
  CASE WHEN instr(all_conversation_tags,'topic:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'topic:')+6, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'topic:')+6),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'topic:')+6),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'topic:')+6)) END)
  END AS topic,
  COUNT(*) AS cnt
FROM intercom__conversation_enhanced
GROUP BY topic ORDER BY cnt DESC