SELECT ce.company_name, ce.plan_name, ce.monthly_spend, ce.created_at
FROM intercom__company_enhanced ce
WHERE ce.company_name = 'River Analytics'
ORDER BY ce.created_at