WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT cp."Event Participation Prize Level", COUNT(*) as cnt
FROM hv 
JOIN customer_tag_table t ON hv."Customer ID"=t."Customer ID"
JOIN campaign_participation_table cp ON t."Contact ID"=cp."Event Participant Contact ID"
GROUP BY cp."Event Participation Prize Level"