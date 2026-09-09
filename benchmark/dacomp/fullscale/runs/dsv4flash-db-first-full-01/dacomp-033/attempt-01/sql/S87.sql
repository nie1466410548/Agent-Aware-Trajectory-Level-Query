WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT s."Ticket customer satisfaction score", COUNT(*) as cnt
FROM hv 
JOIN contracts_table c ON hv."Customer ID"=c."Customer ID"
JOIN service_ticket_table s ON c."Contract ID"=s."Contract ID"
GROUP BY s."Ticket customer satisfaction score"