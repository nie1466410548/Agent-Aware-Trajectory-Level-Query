SELECT company_name, company_id, plan_name, monthly_spend, created_at, updated_at, user_count, session_count
FROM intercom__company_enhanced
WHERE company_name = 'Pioneer Group'
ORDER BY created_at