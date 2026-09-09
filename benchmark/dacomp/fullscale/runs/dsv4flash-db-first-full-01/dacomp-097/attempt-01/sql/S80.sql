-- Topic distribution by segment
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
  CASE 
    WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    ELSE 'other' END AS topic,
  COUNT(*) AS total
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.segment, 2
ORDER BY co.segment, total DESC