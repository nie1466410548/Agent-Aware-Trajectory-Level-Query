WITH sent AS (
  SELECT campaign_id, CAMPAIGN_TYPE, 
         CAST(julianday(scheduled_to_send_at) AS INTEGER) as send_day
  FROM klaviyo__campaigns
  WHERE STATUS = 'SENT'
),
same_type_gaps AS (
  SELECT s1.CAMPAIGN_TYPE as type,
         s2.send_day - s1.send_day as gap_days
  FROM sent s1
  JOIN sent s2 ON s1.CAMPAIGN_TYPE = s2.CAMPAIGN_TYPE 
              AND s2.send_day > s1.send_day
  WHERE NOT EXISTS (
    SELECT 1 FROM sent s3 
    WHERE s3.CAMPAIGN_TYPE = s1.CAMPAIGN_TYPE 
      AND s3.send_day > s1.send_day 
      AND s3.send_day < s2.send_day
  )
)
SELECT type, COUNT(*) as n_intervals, AVG(gap_days) as avg_gap, MIN(gap_days) as min_gap, MAX(gap_days) as max_gap
FROM same_type_gaps
GROUP BY type
ORDER BY avg_gap