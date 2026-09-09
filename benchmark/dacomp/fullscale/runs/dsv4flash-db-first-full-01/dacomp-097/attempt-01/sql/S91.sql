
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
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
),
agg AS (
  SELECT 
    c.company_name,
    COUNT(*) AS num_convs,
    AVG(c.resp_delay) AS avg_resp_delay,
    AVG(c.duration) AS avg_duration,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS bot_ratio
  FROM conv c
  GROUP BY c.company_name
)
SELECT 
  co.seat_bucket,
  AVG(agg.num_convs) AS avg_convs_per_company,
  AVG(agg.avg_resp_delay) AS avg_resp_delay,
  AVG(agg.avg_duration) AS avg_duration,
  AVG(agg.bot_ratio) AS avg_bot_ratio_pct
FROM agg
JOIN company_dim co ON agg.company_name = co.company_name
GROUP BY co.seat_bucket
ORDER BY co.seat_bucket
