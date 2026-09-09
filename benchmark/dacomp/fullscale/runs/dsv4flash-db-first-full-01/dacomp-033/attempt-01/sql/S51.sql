WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT t."Tag Name", COUNT(*) as cnt, AVG(t."Tag Weight Value") as avg_weight
FROM hv JOIN customer_tag_table t ON hv."Customer ID"=t."Customer ID"
GROUP BY t."Tag Name" ORDER BY cnt DESC