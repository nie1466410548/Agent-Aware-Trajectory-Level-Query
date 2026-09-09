WITH hv AS (
  SELECT "Customer ID", SUM(CASE WHEN "Transaction Payment Status"='Paid' THEN "Transaction Amount" ELSE 0 END) as paid_amt,
         COUNT(*) as all_tx, SUM("Transaction Amount") as total_amt_all
  FROM transaction_history_table
  GROUP BY "Customer ID"
  HAVING SUM(CASE WHEN "Transaction Payment Status"='Paid' THEN "Transaction Amount" ELSE 0 END) > 5000
)
SELECT COUNT(*) as hv_customers, SUM(all_tx) as total_tx, SUM(CASE WHEN all_tx>1 THEN 1 ELSE 0 END) as multi_tx_cust, AVG(total_amt_all) as avg_total_amt FROM hv