SELECT 
  CASE 
    WHEN all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    ELSE 'other' END AS topic,
  COUNT(*) AS total,
  ROUND(100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_pct
FROM intercom__conversation_enhanced
GROUP BY 1
ORDER BY total DESC