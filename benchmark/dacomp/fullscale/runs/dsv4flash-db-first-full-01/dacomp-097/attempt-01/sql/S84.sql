-- Topic mix for high-value churn_watch customers (ARR 200k+ or seats 420+)
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN 1 ELSE 0 END AS is_high_arr,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN 1 ELSE 0 END AS is_high_seats
  FROM intercom__company_enhanced
),
conv AS (
  SELECT ce.all_contact_company_names AS company_name, ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
)
SELECT 
  CASE WHEN co.segment='churn_watch' AND (co.is_high_arr=1 OR co.is_high_seats=1) THEN 'high_value_churn_watch'
       WHEN co.segment='new_contract' AND (co.is_high_arr=1 OR co.is_high_seats=1) THEN 'high_value_new_contract'
       ELSE co.segment END AS group_label,
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
WHERE co.segment IN ('churn_watch','new_contract')
GROUP BY 1, 2
ORDER BY 1, total DESC