WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT t."Transaction Currency", COUNT(*) as cnt, SUM(t."Transaction Amount") as total_amt
FROM hv JOIN transaction_history_table t ON hv."Customer ID"=t."Customer ID" AND t."Transaction Payment Status"='Paid'
GROUP BY t."Transaction Currency"