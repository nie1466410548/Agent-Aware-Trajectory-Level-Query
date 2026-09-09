WITH daily AS (
  SELECT strftime('%Y-%m-%d', "Sales Date") AS d, pi."Category Name" AS cat, SUM(s."Sales volume (kg)") AS vol
  FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code"
  GROUP BY d, cat
)
SELECT cat, substr(d,6,2) AS month, ROUND(AVG(vol),1) AS avg_daily_kg
FROM daily GROUP BY cat, month ORDER BY cat, month