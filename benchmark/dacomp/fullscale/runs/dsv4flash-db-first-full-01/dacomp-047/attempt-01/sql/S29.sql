-- Compute profit margin for top July items
SELECT s."Item Code", pi."Item Name", pi."Category Name",
       ROUND(AVG(s."Unit price (yuan/kg)"),2) AS avg_retail,
       ROUND(AVG(pp."Wholesale price (yuan/kg)"),2) AS avg_wholesale,
       ROUND(AVG(s."Unit price (yuan/kg)") - AVG(pp."Wholesale price (yuan/kg)"),2) AS margin,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" END),1) AS july_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
LEFT JOIN purchase_price pp ON s."Item Code"=pp."Item Code" AND date(s."Sales Date")=date(pp."Date")
GROUP BY s."Item Code", pi."Item Name", pi."Category Name"
HAVING july_vol > 100
ORDER BY july_vol DESC
LIMIT 30