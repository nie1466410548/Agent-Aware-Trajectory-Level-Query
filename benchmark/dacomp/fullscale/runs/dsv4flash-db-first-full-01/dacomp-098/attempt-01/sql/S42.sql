
SELECT ce.conversation_initiated_type, ce.sla_name, ce.sla_status, ce.conversation_rating, 
       ce.conversation_remark, cm.time_to_first_response_minutes
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
