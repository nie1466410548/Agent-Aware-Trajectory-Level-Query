-- Topic distribution by segment (churn_watch vs renewal vs new_contract), with bot ratio
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
)
SELECT 
  co.segment,
  CASE 
    WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    ELSE 'other' END AS topic,
  COUNT(*) AS total,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS bot_pct
FROM intercom__conversation_enhanced c
JOIN company_dim co ON c.all_contact_company_names = co.company_name
GROUP BY co.segment, 2
ORDER BY co.segment, total DESC