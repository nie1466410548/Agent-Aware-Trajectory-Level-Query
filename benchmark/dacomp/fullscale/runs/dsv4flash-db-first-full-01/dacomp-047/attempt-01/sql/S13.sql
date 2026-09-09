SELECT s."Item Code", pi."Item Name", pi."Category Name",
       ROUND(SUM(s."Sales volume (kg)"),1) AS total_vol,
       ROUND(AVG(s."Unit price (yuan/kg)"),2) AS avg_price,
       COUNT(DISTINCT s."Sales Date") AS days_sold,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY s."Item Code", pi."Item Name", pi."Category Name"
ORDER BY july_vol DESC
LIMIT 30