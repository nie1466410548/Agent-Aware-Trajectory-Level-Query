WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT cr."Credit Grade", COUNT(*) as cnt, AVG(cr."Credit Score") as avg_score, AVG(cr."Credit Limit") as avg_limit
FROM hv 
JOIN customer_account_table a ON hv."Customer ID"=a."Customer ID"
JOIN customer_credit_rating_table cr ON a."Account ID"=cr."Account ID"
GROUP BY cr."Credit Grade" ORDER BY cnt DESC