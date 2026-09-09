-- Average selling price per item in July
SELECT s."Item Code", pi."Item Name", pi."Category Name",
       ROUND(AVG(s."Unit price (yuan/kg)"),2) AS avg_retail,
       ROUND(AVG(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Unit price (yuan/kg)" END),2) AS july_retail,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" END),1) AS july_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY s."Item Code", pi."Item Name", pi."Category Name"
ORDER BY july_vol DESC
LIMIT 30