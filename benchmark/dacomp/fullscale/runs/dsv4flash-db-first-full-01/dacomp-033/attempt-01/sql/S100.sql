WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT cr."Credit Grade", COUNT(*) as cnt, AVG(cr."Credit Score") as avg_score, AVG(cr."Credit Limit") as avg_limit
FROM hv 
JOIN transaction_history_table t ON hv."Customer ID"=t."Customer ID" AND t."Transaction Payment Status"='Paid'
JOIN customer_credit_rating_table cr ON t."Account ID"=cr."Account ID"
GROUP BY cr."Credit Grade" ORDER BY cnt DESC