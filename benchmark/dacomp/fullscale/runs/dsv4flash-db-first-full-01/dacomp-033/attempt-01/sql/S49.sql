WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT m."Privilege Level", COUNT(*) as cnt
FROM hv JOIN membership_table m ON hv."Customer ID"=m."Customer ID"
GROUP BY m."Privilege Level" ORDER BY cnt DESC