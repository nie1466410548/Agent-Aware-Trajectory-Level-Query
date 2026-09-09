WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT sf."Follow-up Result Status", sf."Follow-up Priority", COUNT(*) as cnt
FROM hv JOIN sales_follow_up_table sf ON hv."Customer ID"=sf."Customer ID"
GROUP BY sf."Follow-up Result Status", sf."Follow-up Priority" ORDER BY cnt DESC