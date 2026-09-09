SELECT COUNT(*), 
  SUM(CASE WHEN time_to_first_response_minutes IS NULL THEN 1 ELSE 0 END) as null_resp,
  SUM(CASE WHEN time_to_last_close_minutes IS NULL THEN 1 ELSE 0 END) as null_close,
  SUM(CASE WHEN time_to_first_close_minutes IS NULL THEN 1 ELSE 0 END) as null_first_close
FROM intercom__conversation_metrics