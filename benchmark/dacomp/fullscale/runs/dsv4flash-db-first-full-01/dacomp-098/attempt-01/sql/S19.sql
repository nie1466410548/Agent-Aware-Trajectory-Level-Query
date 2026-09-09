SELECT DISTINCT 
  CASE WHEN instr(all_conversation_tags,'stage:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'stage:')+6, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'stage:')+6),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'stage:')+6),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'stage:')+6)) END)
  END AS stage,
  COUNT(*) AS cnt
FROM intercom__conversation_enhanced
GROUP BY stage ORDER BY cnt DESC