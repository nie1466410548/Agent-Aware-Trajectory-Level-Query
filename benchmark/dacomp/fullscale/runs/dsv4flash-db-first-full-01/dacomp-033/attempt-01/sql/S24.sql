WITH hv AS (
  SELECT "Customer ID", SUM("Transaction Amount") as paid_amt
  FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT s."Segment Name", COUNT(DISTINCT hv."Customer ID") as hv_customers
FROM hv LEFT JOIN customer_segments_table s ON hv."Customer ID"=s."Customer ID"
GROUP BY s."Segment Name" ORDER BY hv_customers DESC