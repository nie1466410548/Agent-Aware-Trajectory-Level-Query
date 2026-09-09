WITH yearly AS (
  SELECT o.Region, sp."Regional Manager",
         CAST(strftime('%Y', o."Order Date") AS INTEGER) AS yr,
         SUM(o.Sales) AS sales,
         SUM(o.profit) AS profit,
         COUNT(DISTINCT o."Order ID") AS n_orders
  FROM "order" o
  LEFT JOIN salesperson sp ON o.Region = sp.Region
  GROUP BY o.Region, sp."Regional Manager", yr
)
SELECT Region, "Regional Manager", yr, sales, profit, n_orders,
       ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Region ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Region ORDER BY yr), 2) AS yoy_growth_pct
FROM yearly
ORDER BY Region, yr