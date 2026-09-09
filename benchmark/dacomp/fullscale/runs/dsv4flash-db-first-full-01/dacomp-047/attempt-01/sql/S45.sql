-- All items active in 2023, with their July 2022 performance
SELECT s."Item Code", pi."Item Name", pi."Category Name",
       ROUND(SUM(CASE WHEN s."Sales Date">='2023-01-01' THEN s."Sales volume (kg)" ELSE 0 END),1) AS vol_2023,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' AND strftime('%Y', s."Sales Date")='2022' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july22_vol,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' AND strftime('%Y', s."Sales Date")='2021' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july21_vol,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' AND strftime('%Y', s."Sales Date")='2020' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july20_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE s."Sales Date">='2023-01-01'
GROUP BY s."Item Code", pi."Item Name", pi."Category Name"
ORDER BY vol_2023 DESC
LIMIT 40