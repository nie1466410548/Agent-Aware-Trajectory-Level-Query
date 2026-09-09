-- Channel distribution by segment
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
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:email%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS email_pct,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:messenger%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS messenger_pct,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS product_tour_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.segment