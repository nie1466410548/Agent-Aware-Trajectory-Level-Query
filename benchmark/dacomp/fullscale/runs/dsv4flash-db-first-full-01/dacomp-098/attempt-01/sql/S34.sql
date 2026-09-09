SELECT DISTINCT
  CASE WHEN instr(all_conversation_tags,'segment:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'segment:')+8, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'segment:')+8),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'segment:')+8),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'segment:')+8)) END)
  END AS segment,
  COUNT(*) as cnt
FROM intercom__conversation_enhanced
GROUP BY segment ORDER BY cnt DESC