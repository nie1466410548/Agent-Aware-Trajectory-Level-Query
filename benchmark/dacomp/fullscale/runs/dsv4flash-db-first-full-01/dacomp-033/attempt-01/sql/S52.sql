WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT c."Gender", COUNT(*) as cnt
FROM hv JOIN customer_contact_table c ON hv."Customer ID"=c."Customer ID"
GROUP BY c."Gender"