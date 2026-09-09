WITH yearly AS (
  SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
  FROM "order" GROUP BY Category, yr
),
growth AS (
  SELECT Category, yr, sales,
         ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Category ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Category ORDER BY yr), 2) AS yoy_growth_pct
  FROM yearly
),
ranked AS (
  SELECT Category, yr, yoy_growth_pct,
         RANK() OVER (PARTITION BY yr ORDER BY yoy_growth_pct DESC) AS rnk
  FROM growth WHERE yr > 2015
)
SELECT yr, Category, yoy_growth_pct, rnk FROM ranked ORDER BY yr, rnk