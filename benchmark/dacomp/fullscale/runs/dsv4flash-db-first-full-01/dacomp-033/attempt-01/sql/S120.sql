WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT cf."Satisfaction Rating", COUNT(*) as cnt
FROM hv 
JOIN customer_tag_table t ON hv."Customer ID"=t."Customer ID"
JOIN customer_feedback_table cf ON t."Contact ID"=cf."Contact ID"
GROUP BY cf."Satisfaction Rating"