SELECT 
  CASE WHEN all_conversation_tags LIKE '%sla:breached%' THEN 'breached'
       WHEN all_conversation_tags LIKE '%sla:met%' THEN 'met'
       WHEN all_conversation_tags LIKE '%sla:warning%' THEN 'warning' END AS sla_status,
  COUNT(*) AS total,
  ROUND(AVG(time_to_first_response_minutes),2) AS avg_resp_delay,
  ROUND(AVG(time_to_last_close_minutes),2) AS avg_duration
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
GROUP BY 1