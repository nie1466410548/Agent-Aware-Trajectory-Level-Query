WITH yearly AS (
  SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
  FROM "order" GROUP BY Category, yr
)
SELECT Category, yr, sales, ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Category ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Category ORDER BY yr), 2) AS yoy_growth_pct
FROM yearly ORDER BY Category, yr