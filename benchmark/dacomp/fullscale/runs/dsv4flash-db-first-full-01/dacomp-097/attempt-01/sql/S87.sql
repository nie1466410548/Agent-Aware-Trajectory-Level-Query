
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
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
  co.segment,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT c.company_name) AS customers,
  AVG(c.resp_delay) AS avg_resp_delay_min,
  AVG(c.duration) AS avg_duration_min,
  100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*) AS bot_ratio_pct,
  100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) / COUNT(*) AS sla_breach_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.segment
ORDER BY co.segment
