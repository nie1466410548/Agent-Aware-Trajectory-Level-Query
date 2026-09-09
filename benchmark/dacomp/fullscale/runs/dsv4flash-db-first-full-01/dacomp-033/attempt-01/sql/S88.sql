WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT comp."Complaint Customer Satisfaction", COUNT(*) as cnt
FROM hv 
JOIN contracts_table c ON hv."Customer ID"=c."Customer ID"
JOIN service_ticket_table s ON c."Contract ID"=s."Contract ID"
JOIN complaints_table comp ON s."Work Order ID"=comp."Work Order ID"
GROUP BY comp."Complaint Customer Satisfaction"