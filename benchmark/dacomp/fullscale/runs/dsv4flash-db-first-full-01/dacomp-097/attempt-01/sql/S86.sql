
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         ELSE 'unknown' END AS arr_bucket,
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
    SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS bot_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS sla_breach_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS product_tour_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS usage_insight_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS adoption_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS escalation_ratio
  FROM conv c
  GROUP BY c.company_name
)
SELECT 
  a.*, co.segment, co.arr_bucket, co.seat_bucket,
  cm.registration_retention_7d AS ret_7d,
  cm.registration_retention_30d AS ret_30d,
  cm.contacts_active_7d AS active_7d,
  cm.contacts_active_30d AS active_30d
FROM agg a
JOIN company_dim co ON a.company_name = co.company_name
JOIN intercom__company_metrics cm ON a.company_name = cm.company_name
