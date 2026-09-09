WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT ct."Contract Type", COUNT(*) as cnt
FROM hv JOIN contracts_table ct ON hv."Customer ID"=ct."Customer ID"
GROUP BY ct."Contract Type" ORDER BY cnt DESC