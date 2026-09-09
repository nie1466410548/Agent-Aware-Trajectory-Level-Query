-- Conversation-to-Feature-Usage Conversion Rate - fixed
WITH company_dim AS (
  SELECT DISTINCT company_name FROM intercom__company_enhanced
),
contacts AS (
  SELECT DISTINCT all_contact_company_names AS company_name FROM intercom__contact_enhanced
),
conv_end AS (
  SELECT 
    all_contact_company_names AS company_name,
    last_close_at
  FROM intercom__conversation_enhanced
  WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT 
    all_contact_company_names AS company_name,
    last_activity_ts
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
  (SELECT COUNT(*) FROM contacts) AS total_customers,
  (SELECT COUNT(DISTINCT company_name) FROM conv_end) AS customers_with_convs,
  (SELECT COUNT(*) FROM converted) AS customers_converted,
  ROUND(100.0 * (SELECT COUNT(*) FROM converted) / (SELECT COUNT(*) FROM contacts), 2) AS conversion_rate_pct