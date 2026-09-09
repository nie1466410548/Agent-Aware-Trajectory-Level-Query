SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count, SUM("Sales Amount") AS total_spent
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Product Code", "Customer ID"
ORDER BY "Product Code", purchase_count DESC