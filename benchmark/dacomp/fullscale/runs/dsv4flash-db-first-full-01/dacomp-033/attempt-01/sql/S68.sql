SELECT a."Account Type", COUNT(DISTINCT t."Customer ID") as hv_customers
FROM (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000) hv
LEFT JOIN customer_account_table a ON hv."Customer ID"=a."Customer ID"
GROUP BY a."Account Type"