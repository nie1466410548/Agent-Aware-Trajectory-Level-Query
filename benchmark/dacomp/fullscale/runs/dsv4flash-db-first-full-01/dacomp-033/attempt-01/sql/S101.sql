SELECT cr."Credit Grade", COUNT(*) as cnt, AVG(cr."Credit Score") as avg_score, AVG(cr."Credit Limit") as avg_limit
FROM customer_credit_rating_table cr 
JOIN (SELECT DISTINCT "Account ID" FROM transaction_history_table) t ON t."Account ID"=cr."Account ID"
GROUP BY cr."Credit Grade" ORDER BY cnt DESC