-- Check the distribution of key metrics
SELECT
  MIN(count_active_days) AS min_days, 
  AVG(count_active_days) AS avg_days, 
  MAX(count_active_days) AS max_days,
  MIN(sum_minutes) AS min_min, 
  AVG(sum_minutes) AS avg_min, 
  MAX(sum_minutes) AS max_min,
  MIN(sum_events) AS min_evt, 
  AVG(sum_events) AS avg_evt, 
  MAX(sum_events) AS max_evt,
  MIN(avg_nps_rating) AS min_nps, 
  AVG(avg_nps_rating) AS avg_nps, 
  MAX(avg_nps_rating) AS max_nps
FROM pendo__account