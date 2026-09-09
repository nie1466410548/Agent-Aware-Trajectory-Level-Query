WITH hv AS (
  SELECT "Customer ID", SUM("Transaction Amount") as paid_amt
  FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT t."Tag Name", COUNT(DISTINCT hv."Customer ID") as hv_customers, SUM(t."Tag Weight Value") as tot_weight
FROM hv LEFT JOIN customer_tag_table t ON hv."Customer ID"=t."Customer ID"
GROUP BY t."Tag Name" ORDER BY hv_customers DESC