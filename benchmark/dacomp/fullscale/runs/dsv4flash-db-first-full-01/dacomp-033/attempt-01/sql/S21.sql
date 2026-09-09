WITH hv AS (
  SELECT "Customer ID", SUM("Transaction Amount") as paid_amt, COUNT(*) as n_tx
  FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT m."Membership Level", COUNT(DISTINCT hv."Customer ID") as hv_customers
FROM hv LEFT JOIN membership_table m ON hv."Customer ID"=m."Customer ID"
GROUP BY m."Membership Level" ORDER BY hv_customers DESC