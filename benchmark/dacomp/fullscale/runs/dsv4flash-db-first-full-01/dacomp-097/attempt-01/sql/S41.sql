-- Check time_to_first_response_minutes distribution for outlier detection
SELECT 
  COUNT(*) as total,
  AVG(time_to_first_response_minutes) as avg,
  MIN(time_to_first_response_minutes) as min_val,
  MAX(time_to_first_response_minutes) as max_val
FROM intercom__conversation_metrics
WHERE time_to_first_response_minutes IS NOT NULL