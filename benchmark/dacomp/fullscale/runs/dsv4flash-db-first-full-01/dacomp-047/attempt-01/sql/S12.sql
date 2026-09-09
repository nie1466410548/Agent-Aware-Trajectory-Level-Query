WITH item_monthly AS (
  SELECT s."Item Code", pi."Item Name", pi."Category Name",
         strftime('%m', s."Sales Date") AS mo,
         SUM(s."Sales volume (kg)") AS vol_kg
  FROM sales_records s
  JOIN product_information pi ON s."Item Code"=pi."Item Code"
  GROUP BY s."Item Code", pi."Item Name", pi."Category Name", mo
)
SELECT * FROM item_monthly
WHERE mo = '07'
ORDER BY vol_kg DESC
LIMIT 30