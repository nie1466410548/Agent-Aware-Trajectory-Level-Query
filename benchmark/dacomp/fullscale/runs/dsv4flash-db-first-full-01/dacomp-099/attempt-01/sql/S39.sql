SELECT plan_name, COUNT(*) as n, ROUND(AVG(monthly_spend),0) as avg_spend, ROUND(MIN(monthly_spend),0) as min_spend, ROUND(MAX(monthly_spend),0) as max_spend, ROUND(AVG(session_count),0) as avg_sessions, ROUND(AVG(user_count),0) as avg_users
FROM intercom__company_enhanced
GROUP BY plan_name
ORDER BY avg_spend