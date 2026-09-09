WITH yearly AS (
  SELECT o.Region, sp."Regional Manager",
         CAST(strftime('%Y', o."Order Date") AS INTEGER) AS yr,
         SUM(o.Sales) AS sales
  FROM "order" o
  LEFT JOIN salesperson sp ON o.Region = sp.Region
  GROUP BY o.Region, sp."Regional Manager", yr
)
SELECT Region, "Regional Manager", yr, ROUND(sales,2) AS sales,
       ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Region ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Region ORDER BY yr), 2) AS yoy_growth_pct,
       ROUND(100.0 * (sales - FIRST_VALUE(sales) OVER (PARTITION BY Region ORDER BY yr)) / FIRST_VALUE(sales) OVER (PARTITION BY Region ORDER BY yr), 2) AS cum_growth_vs_2015_pct
FROM yearly
WHERE Region IN ('Northeast','Southwest','Northwest')
ORDER BY Region, yr