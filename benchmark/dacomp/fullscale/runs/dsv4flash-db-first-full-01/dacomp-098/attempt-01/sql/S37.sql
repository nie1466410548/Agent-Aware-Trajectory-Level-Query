WITH conv AS (
  SELECT 
    ce.all_conversation_contacts AS contact_id,
    ce.conversation_id,
    ce.conversation_created_at,
    ce.conversation_initiated_type,
    cm.first_admin_response_at,
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
    END AS intent,
    CASE WHEN instr(ce.all_conversation_tags,'topic:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'topic:')+6,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6)) END)
    END AS topic,
    CASE WHEN instr(ce.all_conversation_tags,'region:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'region:')+7,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7)) END)
    END AS region
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
),
staged AS (
  SELECT *,
    CASE stage
      WHEN 'contacted' THEN 1
      WHEN 'marketing_qualified' THEN 2
      WHEN 'trial_started' THEN 3
      WHEN 'demo_booked' THEN 4
      WHEN 'trial_activated' THEN 5
      WHEN 'proposal_sent' THEN 6
      WHEN 'closed_won' THEN 7
      WHEN 'expansion_in_flight' THEN 8
      WHEN 'closed_lost' THEN 99
      ELSE 0
    END AS stage_rank
  FROM conv
)
SELECT contact_id,
  MIN(CASE WHEN stage_rank>=1 AND stage_rank<99 THEN stage_rank END) AS min_reached,
  MAX(CASE WHEN stage_rank>=1 AND stage_rank<99 THEN stage_rank END) AS max_reached,
  MIN(CASE WHEN stage_rank=99 THEN 1 ELSE 0 END) AS has_lost,
  COUNT(*) AS n_conv
FROM staged
GROUP BY contact_id
LIMIT 15