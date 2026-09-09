WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT po."Current Service Status", COUNT(*) as cnt, SUM(po."Total Amount") as tot_amt
FROM hv JOIN product_service_order_table po ON hv."Customer ID"=po."Customer ID"
GROUP BY po."Current Service Status" ORDER BY cnt DESC