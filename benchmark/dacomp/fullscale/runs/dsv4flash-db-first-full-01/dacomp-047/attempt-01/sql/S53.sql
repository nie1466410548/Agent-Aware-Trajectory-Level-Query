-- Check the correlation between Water Spinach (portion) and Water Spinach - are they the same product?
-- Also check if Water Spinach is still sold in 2023
SELECT pi."Item Name", strftime('%Y', s."Sales Date") AS yr, ROUND(SUM(s."Sales volume (kg)"),1) AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Water Spinach','Water Spinach (portion)','Sweet Potato Vine Tips','Sweet Potato Vine Tips (portion)')
GROUP BY pi."Item Name", yr
ORDER BY pi."Item Name", yr