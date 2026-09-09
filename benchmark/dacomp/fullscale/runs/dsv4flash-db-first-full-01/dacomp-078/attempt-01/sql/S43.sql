-- Check correlation between duration, frequency, and other metrics
-- First, let's see the percentile distribution of key metrics
SELECT
  ROUND((count_active_days - 1.0) / 10) * 10 AS days_bucket,
  COUNT(*) AS cnt,
  AVG(sum_minutes) AS avg_min,
  AVG(sum_events) AS avg_events,
  AVG(avg_nps_rating) AS avg_nps,
  AVG(count_associated_visitors) AS avg_visitors
FROM pendo__account
GROUP BY days_bucket
ORDER BY days_bucket