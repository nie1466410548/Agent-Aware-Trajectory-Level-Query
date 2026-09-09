-- Conversation-to-Feature-Usage Conversion Rate
-- Proxy: a company counts as converted if any contact had activity (last_activity_ts) within 72h after a conversation ended (last_close_at)
WITH conv_end AS (
  SELECT 
    all_contact_company_names AS company_name,
    conversation_id,
    julianday(last_close_at) * 24 AS close_hr,
    julianday(last_close_at) * 24 + 72 AS close_hr_72
  FROM intercom__conversation_enhanced
  WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT 
    all_contact_company_names AS company_name,
    julianday(last_activity_ts) * 24 AS act_hr
  FROM intercom__contact_enhanced
  WHERE last_activity_ts IS NOT NULL
),
converted AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c
  JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.act_hr >= c.close_hr AND a.act_hr <= c.close_hr_72
),
all_cust AS (
  SELECT DISTINCT company_name FROM intercom__contact_enhanced
)
SELECT 
  COUNT(DISTINCT conv_end.company_name) AS customers_with_convs,
  (SELECT COUNT(DISTINCT company_name) FROM all_cust) AS total_customers,
  (SELECT COUNT(DISTINCT company_name) FROM converted) AS customers_converted,
  ROUND(100.0 * (SELECT COUNT(DISTINCT company_name) FROM converted) / (SELECT COUNT(DISTINCT company_name) FROM all_cust), 2) AS conversion_rate_pct
FROM conv_end