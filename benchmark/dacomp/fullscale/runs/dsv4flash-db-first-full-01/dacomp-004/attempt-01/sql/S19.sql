SELECT "Sales Month", "Product Code",
       COUNT(DISTINCT "Customer ID") AS cust_n,
       COUNT(*) AS txn_n,
       ROUND(1.0 * (COUNT(*) - COUNT(DISTINCT "Customer ID")) / COUNT(*), 4) AS repeat_txn_share
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Sales Month", "Product Code"
ORDER BY "Product Code", "Sales Month"