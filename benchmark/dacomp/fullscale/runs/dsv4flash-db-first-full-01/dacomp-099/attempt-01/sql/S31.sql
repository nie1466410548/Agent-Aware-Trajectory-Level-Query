SELECT company_name, COUNT(DISTINCT company_id) as cnt, COUNT(DISTINCT plan_name) as plan_cnt, GROUP_CONCAT(DISTINCT plan_name) as plans, GROUP_CONCAT(DISTINCT monthly_spend) as spends
FROM intercom__company_enhanced
GROUP BY company_name
HAVING cnt > 1
ORDER BY cnt DESC
LIMIT 30