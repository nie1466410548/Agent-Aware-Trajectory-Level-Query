SELECT "Major Category Name", "Intermediate Category Name", "Sales Month", ROUND(SUM("Sales Amount"),2) AS monthly_amount, SUM("Sales Quantity") AS monthly_qty
FROM sheet1
WHERE "Major Category Name" IN ('Meat and poultry', 'Instant mixes', 'Cooked food', 'Aquatic Products', 'Knitwear', 'Stationery and Sports', 'Home appliances', 'Baking', 'Household')
GROUP BY "Major Category Name", "Intermediate Category Name", "Sales Month"
ORDER BY "Major Category Name", "Intermediate Category Name", "Sales Month"