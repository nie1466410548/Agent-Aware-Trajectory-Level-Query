WITH cust AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count
  FROM sheet1
  WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
  GROUP BY "Product Code", "Customer ID"
)
SELECT "Product Code",
       COUNT(*) AS n_customers,
       SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
       ROUND(1.0 * SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) / COUNT(*), 4) AS customer_repurchase_rate,
       SUM(purchase_count) AS n_transactions,
       ROUND(1.0 * (SUM(purchase_count) - COUNT(*)) / SUM(purchase_count), 4) AS transaction_repurchase_share
FROM cust
GROUP BY "Product Code"
ORDER BY "Product Code"