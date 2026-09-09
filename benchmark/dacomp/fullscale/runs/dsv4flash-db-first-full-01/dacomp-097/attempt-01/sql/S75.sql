-- Topic distribution
SELECT 
  CASE 
    WHEN all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN all_conversation_tags LIKE '%topic:product%' THEN 'product'
    ELSE 'other'
  END AS topic,
  COUNT(*) AS total
FROM intercom__conversation_enhanced
GROUP BY 1
ORDER BY total DESC