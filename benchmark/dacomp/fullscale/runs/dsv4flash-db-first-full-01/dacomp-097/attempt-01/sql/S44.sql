-- Check how many conversations fall outside P1/P99 bounds
SELECT 
  SUM(CASE WHEN time_to_first_response_minutes < 11 OR time_to_first_response_minutes > 42 THEN 1 ELSE 0 END) AS resp_outliers,
  SUM(CASE WHEN time_to_last_close_minutes < 91 OR time_to_last_close_minutes > 1030 THEN 1 ELSE 0 END) AS dur_outliers
FROM intercom__conversation_metrics