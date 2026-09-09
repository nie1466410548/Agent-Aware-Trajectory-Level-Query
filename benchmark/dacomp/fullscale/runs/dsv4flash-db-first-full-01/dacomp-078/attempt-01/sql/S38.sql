-- Check feature usage metrics distribution
SELECT 
  MIN(average_daily_minutes) AS min_avg_daily_min,
  AVG(average_daily_minutes) AS avg_avg_daily_min,
  MAX(average_daily_minutes) AS max_avg_daily_min,
  MIN(average_daily_events) AS min_avg_daily_evt,
  AVG(average_daily_events) AS avg_avg_daily_evt,
  MAX(average_daily_events) AS max_avg_daily_evt,
  COUNT(CASE WHEN avg_nps_rating IS NOT NULL THEN 1 END) AS nps_not_null,
  COUNT(CASE WHEN avg_nps_rating IS NULL THEN 1 END) AS nps_null
FROM pendo__account