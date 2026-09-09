SELECT cr."Credit Grade", COUNT(*) as cnt_all, AVG(cr."Credit Score") as avg_score_all, AVG(cr."Credit Limit") as avg_limit_all
FROM customer_credit_rating_table cr 
GROUP BY cr."Credit Grade" ORDER BY cnt_all DESC