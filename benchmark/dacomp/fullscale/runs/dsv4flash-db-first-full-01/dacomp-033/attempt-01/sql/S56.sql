WITH hv AS (
  SELECT "Customer ID", SUM("Transaction Amount") as paid_amt, COUNT(*) as n_tx
  FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT 
  MIN(paid_amt) as min_amt, 
  MAX(paid_amt) as max_amt, 
  AVG(paid_amt) as avg_amt,
  SUM(paid_amt) as total_amt,
  COUNT(*) as n_customers,
  AVG(n_tx) as avg_tx_count
FROM hv