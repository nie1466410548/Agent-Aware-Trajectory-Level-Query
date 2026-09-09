-- Daily sales per category for correlation analysis
SELECT strftime('%Y-%m-%d', s."Sales Date") AS d,
       pi."Category Name" AS cat,
       SUM(s."Sales volume (kg)") AS daily_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY d, cat
ORDER BY d, cat LIMIT 30