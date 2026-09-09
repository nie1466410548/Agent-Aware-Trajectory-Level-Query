SELECT 
  strftime('%Y-%m', conversation_created_at) AS month,
  COUNT(*) AS total_convs,
  ROUND(AVG(time_to_first_response_minutes),2) AS avg_resp_delay,
  ROUND(AVG(time_to_last_close_minutes),2) AS avg_duration,
  ROUND(100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_pct
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
  AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
GROUP BY strftime('%Y-%m', conversation_created_at)
ORDER BY month