SELECT "Profit Margin", "Total Logistics Revenue", "Profit", "Total Logistics Cost"
FROM sheet1 WHERE "Destination" LIKE 'South China%' AND "Profit Margin" > 1
ORDER BY "Profit Margin" DESC LIMIT 20