-- Bot vs human response times
SELECT 
  CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 'bot' ELSE 'human' END AS responder,
  COUNT(*) AS total,
  ROUND(AVG(time_to_first_response_minutes), 2) AS avg_resp_min,
  ROUND(AVG(time_to_last_close_minutes), 2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_breached_pct
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
GROUP BY 1