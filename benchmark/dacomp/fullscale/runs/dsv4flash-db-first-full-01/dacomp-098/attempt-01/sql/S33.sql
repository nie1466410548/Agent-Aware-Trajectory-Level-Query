SELECT DISTINCT
  CASE WHEN instr(all_conversation_tags,'path:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'path:')+5, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5)) END)
  END AS path,
  CASE WHEN instr(all_conversation_tags,'lifecycle:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'lifecycle:')+10, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10)) END)
  END AS lifecycle,
  COUNT(*) as cnt
FROM intercom__conversation_enhanced
GROUP BY path, lifecycle ORDER BY cnt DESC