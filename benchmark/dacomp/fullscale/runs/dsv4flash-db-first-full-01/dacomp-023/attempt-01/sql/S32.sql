WITH yearly AS (
  SELECT o.Region, CAST(strftime('%Y', o."Order Date") AS INTEGER) AS yr,
         SUM(o.Sales) AS sales, COUNT(DISTINCT o."Order ID") AS n_orders
  FROM "order" o GROUP BY o.Region, yr
),
growth AS (
  SELECT Region, yr, sales, n_orders,
         ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Region ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Region ORDER BY yr), 2) AS yoy_sales_growth,
         ROUND(100.0 * (n_orders - LAG(n_orders) OVER (PARTITION BY Region ORDER BY yr)) / LAG(n_orders) OVER (PARTITION BY Region ORDER BY yr), 2) AS yoy_order_growth
  FROM yearly
)
SELECT g.*, sp."Regional Manager"
FROM growth g
LEFT JOIN salesperson sp ON g.Region = sp.Region
WHERE yr > 2015
ORDER BY g.Region, g.yr