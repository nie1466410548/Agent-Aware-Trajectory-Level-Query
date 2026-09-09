-- Overall metrics with proper dedup
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE 
      WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
      WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
      WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
      WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
      ELSE 'unknown' END AS segment,
    CASE 
      WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
      WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
      WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
      WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
      WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
      ELSE 'unknown' END AS seat_bucket,
    CASE 
      WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
      ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.conversation_id,
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags,
    cm.conversation_created_at,
    ce.last_close_at
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes >= 91 AND cm.time_to_last_close_minutes <= 1030
    AND cm.time_to_first_response_minutes >= 11 AND cm.time_to_first_response_minutes <= 42
)
SELECT 
  'OVERALL' AS slice_type,
  'ALL' AS slice_value,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT company_name) AS total_customers,
  ROUND(AVG(resp_delay), 2) AS avg_resp_delay_min,
  ROUND(AVG(duration), 2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_ratio_pct
FROM conv