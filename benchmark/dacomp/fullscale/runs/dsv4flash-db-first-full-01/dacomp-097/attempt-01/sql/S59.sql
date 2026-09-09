-- Metrics by seat bucket
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.conversation_id, ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
)
SELECT 
  co.seat_bucket,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT c.company_name) AS customers,
  ROUND(AVG(c.resp_delay), 2) AS avg_resp_delay_min,
  ROUND(AVG(c.duration), 2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_ratio_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.seat_bucket
ORDER BY co.seat_bucket