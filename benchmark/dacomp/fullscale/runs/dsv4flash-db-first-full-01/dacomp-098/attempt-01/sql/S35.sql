SELECT conversation_initiated_type, 
  CASE WHEN instr(all_conversation_tags,'path:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'path:')+5, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5)) END)
  END AS path_tag,
  COUNT(*) as cnt
FROM intercom__conversation_enhanced
GROUP BY conversation_initiated_type, path_tag