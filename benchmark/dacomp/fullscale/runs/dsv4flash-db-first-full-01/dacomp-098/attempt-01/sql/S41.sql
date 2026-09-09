
SELECT 
  ce.all_conversation_contacts AS contact_id,
  ce.conversation_id,
  ce.conversation_created_at,
  ce.conversation_initiated_type,
  ce.conversation_subject,
  ce.sla_name,
  ce.sla_status,
  ce.conversation_rating,
  ce.conversation_state,
  ce.all_conversation_tags,
  cm.count_total_parts,
  cm.count_reopens,
  cm.time_to_first_response_minutes,
  CASE WHEN instr(ce.all_conversation_tags,'stage:')>0 THEN
    substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'stage:')+6,
      CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')>0
        THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')-1
        ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6)) END)
  END AS stage,
  CASE WHEN instr(ce.all_conversation_tags,'intent:')>0 THEN
    substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'intent:')+7,
      CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')>0
        THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')-1
        ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7)) END)
  END AS intent
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
