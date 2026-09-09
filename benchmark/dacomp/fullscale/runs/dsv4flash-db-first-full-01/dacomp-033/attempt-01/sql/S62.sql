WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT cs."Channel Name", COUNT(*) as cnt
FROM hv JOIN channel_source_table cs ON hv."Customer ID"=cs."Customer ID"
GROUP BY cs."Channel Name" ORDER BY cnt DESC LIMIT 15