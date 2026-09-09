SELECT ce.company_name, ce.plan_name, ce.created_at, ce.updated_at, ce.monthly_spend, ce.user_count, ce.session_count
FROM intercom__company_enhanced ce
WHERE ce.company_name = 'Edge Platforms'
ORDER BY ce.created_at