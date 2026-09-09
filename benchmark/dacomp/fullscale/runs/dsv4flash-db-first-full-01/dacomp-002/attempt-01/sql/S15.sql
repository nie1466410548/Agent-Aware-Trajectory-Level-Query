-- Monthly breakdown at intermediate category level for top major categories
SELECT "Major Category Name", "Intermediate Category Name", "Sales Month", ROUND(SUM("Sales Amount"),2) AS monthly_amount, SUM("Sales Quantity") AS monthly_qty
FROM sheet1
WHERE "Major Category Name" IN ('Vegetables and fruits','Daily fresh products','Leisure','Grain and oil','Alcoholic beverages','Household & Personal Care')
GROUP BY "Major Category Name", "Intermediate Category Name", "Sales Month"
ORDER BY "Major Category Name", "Intermediate Category Name", "Sales Month"