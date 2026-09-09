-- Conversation-to-feature-usage conversion by topic (company-level)
WITH conv_end AS (
  SELECT DISTINCT all_contact_company_names AS company_name, last_close_at
  FROM intercom__conversation_enhanced
  WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT all_contact_company_names AS company_name, last_activity_ts
  FROM intercom__contact_enhanced
  WHERE last_activity_ts IS NOT NULL
),
converted_companies AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.last_activity_ts >= c.last_close_at 
    AND a.last_activity_ts <= datetime(c.last_close_at, '+72 hours')
)
SELECT 
  CASE 
    WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    ELSE 'other' END AS topic,
  COUNT(DISTINCT c.all_contact_company_names) AS companies_with_topic,
  COUNT(DISTINCT CASE WHEN cv.company_name IS NOT NULL THEN c.all_contact_company_names END) AS converted_companies
FROM intercom__conversation_enhanced c
LEFT JOIN converted_companies cv ON c.all_contact_company_names = cv.company_name
GROUP BY 1
ORDER BY 2 DESC