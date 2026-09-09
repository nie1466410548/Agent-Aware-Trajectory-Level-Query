-- Overall and segment-level metrics: response delay, bot ratio, volume
WITH company_dim AS (
  SELECT 
    company_id, company_name,
    CASE 
      WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
      WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
      WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
      WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
      ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.conversation_id,
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
),
merged AS (
  SELECT c.*, co.segment
  FROM conv c JOIN company_dim co ON c.company_name = co.company_name
)
SELECT 
  COALESCE(segment, 'ALL') AS segment,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT company_name) AS customers,
  ROUND(AVG(resp_delay),2) AS avg_resp_delay_min,
  ROUND(AVG(CASE WHEN resp_delay IS NOT NULL THEN resp_delay END),2) AS avg_resp,
  ROUND(AVG(duration),2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_ratio_pct
FROM merged
GROUP BY segment
ORDER BY segment