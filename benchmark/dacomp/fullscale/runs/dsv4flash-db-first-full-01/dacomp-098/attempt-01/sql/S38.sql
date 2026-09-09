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
    END AS region,
    CASE WHEN instr(ce.all_conversation_tags,'segment:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'segment:')+8,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8)) END)
    END AS segment
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
),
first_contact AS (
  SELECT contact_id, ROW_NUMBER() OVER (PARTITION BY contact_id ORDER BY conversation_created_at) AS rn,
    conversation_created_at AS first_conv_at,
    conversation_initiated_type AS first_type,
    first_admin_response_at AS first_response_at,
    time_to_first_response_minutes AS first_response_mins,
    stage, stage_rank, intent, topic, region, segment
  FROM staged
),
first_conv AS (
  SELECT * FROM first_contact WHERE rn = 1
),
milestones AS (
  SELECT contact_id,
    MAX(CASE WHEN stage_rank>=1 AND stage_rank<99 THEN stage_rank END) AS max_stage_rank,
    MIN(CASE WHEN stage_rank>=4 AND stage_rank<99 THEN conversation_created_at END) AS demo_booked_at,
    MIN(CASE WHEN stage_rank>=5 AND stage_rank<99 THEN conversation_created_at END) AS trial_activated_at,
    MIN(CASE WHEN stage_rank>=7 AND stage_rank<99 THEN conversation_created_at END) AS paid_at
  FROM staged
  GROUP BY contact_id
)
SELECT 
  fc.contact_id,
  fc.first_type,
  fc.first_conv_at,
  fc.first_response_at,
  fc.first_response_mins,
  fc.intent,
  fc.topic,
  fc.region,
  fc.segment,
  fc.stage AS first_stage,
  fc.stage_rank AS first_stage_rank,
  ms.max_stage_rank,
  ms.demo_booked_at,
  ms.trial_activated_at,
  ms.paid_at,
  CASE WHEN ms.demo_booked_at IS NOT NULL THEN 1 ELSE 0 END AS reached_demo,
  CASE WHEN ms.trial_activated_at IS NOT NULL THEN 1 ELSE 0 END AS reached_trial,
  CASE WHEN ms.paid_at IS NOT NULL THEN 1 ELSE 0 END AS reached_paid
FROM first_conv fc
LEFT JOIN milestones ms ON fc.contact_id = ms.contact_id
ORDER BY fc.contact_id