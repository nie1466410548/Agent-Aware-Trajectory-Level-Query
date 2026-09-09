SELECT 
  CASE WHEN instr(all_conversation_tags,'lifecycle:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'lifecycle:')+10, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10)) END)
  END AS lifecycle,
  COUNT(*) as cnt
FROM intercom__conversation_enhanced
GROUP BY lifecycle ORDER BY cnt DESC