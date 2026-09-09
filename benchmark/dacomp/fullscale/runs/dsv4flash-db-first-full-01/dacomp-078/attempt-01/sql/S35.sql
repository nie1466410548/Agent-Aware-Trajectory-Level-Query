-- Distribution of last_event_on to understand churn patterns
SELECT 
  CASE 
    WHEN last_event_on >= '2024-07-01' THEN 'Active_Jul_Oct'
    WHEN last_event_on >= '2024-04-01' THEN 'Active_Apr_Jun'
    ELSE 'Active_Jan_Mar'
  END AS activity_period,
  COUNT(*) AS accounts,
  AVG(sum_minutes) AS avg_minutes,
  AVG(sum_events) AS avg_events,
  AVG(count_active_days) AS avg_active_days,
  AVG(count_active_months) AS avg_active_months,
  AVG(avg_nps_rating) AS avg_nps,
  AVG(count_associated_visitors) AS avg_visitors
FROM pendo__account
GROUP BY activity_period
ORDER BY activity_period