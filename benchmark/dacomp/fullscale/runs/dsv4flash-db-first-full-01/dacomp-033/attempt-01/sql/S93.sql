WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT AVG(m."Current Points") as avg_cur, AVG(m."Lifetime Points") as avg_life, MIN(m."Lifetime Points") as min_life, MAX(m."Lifetime Points") as max_life
FROM hv JOIN membership_table m ON hv."Customer ID"=m."Customer ID"