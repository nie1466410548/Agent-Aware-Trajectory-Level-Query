-- Bot ratio and SLA by segment
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
  SELECT ce.all_contact_company_names AS company_name, ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
)
SELECT 
  co.segment,
  COUNT(*) AS total_convs,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS bot_pct,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_breached_pct,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:met%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_met_pct,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:warning%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_warning_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.segment