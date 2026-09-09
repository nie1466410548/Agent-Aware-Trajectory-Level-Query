WITH sent AS (
  SELECT campaign_id, CAMPAIGN_TYPE, scheduled_to_send_at,
         ROW_NUMBER() OVER (ORDER BY scheduled_to_send_at) as seq
  FROM klaviyo__campaigns
  WHERE STATUS = 'SENT'
),
gaps AS (
  SELECT s1.CAMPAIGN_TYPE as type,
         CAST(julianday(s2.scheduled_to_send_at) - julianday(s1.scheduled_to_send_at) AS INTEGER) as gap_days
  FROM sent s1
  JOIN sent s2 ON s2.seq = s1.seq + 1
)
SELECT type, COUNT(*) as n_sends, AVG(gap_days) as avg_gap_days, MIN(gap_days) as min_gap, MAX(gap_days) as max_gap
FROM gaps
GROUP BY type
ORDER BY n_sends DESC