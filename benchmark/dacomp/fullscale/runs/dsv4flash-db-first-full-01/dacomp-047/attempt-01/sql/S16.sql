SELECT pi."Category Name",
       AVG(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" END) AS july_avg,
       AVG(s."Sales volume (kg)") AS overall_avg,
       (AVG(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" END) / AVG(s."Sales volume (kg)")) * 100 AS july_seasonality_idx
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY pi."Category Name"
ORDER BY july_seasonality_idx DESC