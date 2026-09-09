WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT f."Outstanding Amount" as outstanding, COUNT(*) as cnt, AVG(f."Outstanding Amount") as avg_out, AVG(f."Amount Received") as avg_recv, AVG(f."Receivable Amount") as avg_recvbl
FROM hv JOIN financials_table f ON hv."Customer ID"=f."Customer ID"
GROUP BY f."Outstanding Amount" ORDER BY cnt DESC