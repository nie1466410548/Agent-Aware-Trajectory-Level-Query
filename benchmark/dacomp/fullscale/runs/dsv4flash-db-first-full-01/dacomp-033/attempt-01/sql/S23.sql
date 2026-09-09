WITH hv AS (
  SELECT "Customer ID", SUM("Transaction Amount") as paid_amt
  FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT c."Credit Grade", COUNT(DISTINCT hv."Customer ID") as hv_customers, AVG(c."Credit Score") as avg_score
FROM hv LEFT JOIN customer_account_table a ON hv."Customer ID"=a."Customer ID"
LEFT JOIN customer_credit_rating_table c ON a."Account ID"=c."Account ID"
GROUP BY c."Credit Grade" ORDER BY hv_customers DESC