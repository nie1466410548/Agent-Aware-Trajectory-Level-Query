
SELECT ce.company_name, ce.plan_name, ce.monthly_spend, cm.*
FROM intercom__company_enhanced ce
JOIN intercom__company_metrics cm ON ce.company_id = cm.company_id
