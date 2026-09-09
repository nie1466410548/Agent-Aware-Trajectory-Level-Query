-- Topic mix for churn_watch companies with high ARR (200k+)
SELECT 
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
FROM intercom__conversation_enhanced c
JOIN intercom__company_enhanced co ON c.all_contact_company_names = co.company_name
WHERE co.all_company_tags LIKE '%segment:churn_watch%' 
  AND co.all_company_tags LIKE '%arr_bucket:arr:200k_plus%'
GROUP BY 1
ORDER BY total DESC