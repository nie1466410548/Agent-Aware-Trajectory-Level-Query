-- Conversion rate by segment
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv_end AS (
  SELECT DISTINCT all_contact_company_names AS company_name, last_close_at
  FROM intercom__conversation_enhanced
  WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT all_contact_company_names AS company_name, last_activity_ts
  FROM intercom__contact_enhanced
  WHERE last_activity_ts IS NOT NULL
),
converted AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c
  JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.last_activity_ts >= c.last_close_at 
    AND a.last_activity_ts <= datetime(c.last_close_at, '+72 hours')
)
SELECT 
  cd.segment,
  COUNT(DISTINCT cd.company_name) AS total_customers,
  COUNT(DISTINCT conv.company_name) AS customers_with_convs,
  COUNT(DISTINCT cv.company_name) AS customers_converted,
  ROUND(100.0 * COUNT(DISTINCT cv.company_name) / COUNT(DISTINCT cd.company_name), 2) AS conversion_rate_pct
FROM company_dim cd
LEFT JOIN (SELECT DISTINCT company_name FROM conv_end) conv ON cd.company_name = conv.company_name
LEFT JOIN converted cv ON cd.company_name = cv.company_name
GROUP BY cd.segment
ORDER BY cd.segment