-- Metrics by ARR bucket
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         ELSE 'unknown' END AS arr_bucket
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
  co.arr_bucket,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT c.company_name) AS customers,
  ROUND(AVG(c.resp_delay), 2) AS avg_resp_delay_min,
  ROUND(AVG(c.duration), 2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_ratio_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.arr_bucket
ORDER BY co.arr_bucket