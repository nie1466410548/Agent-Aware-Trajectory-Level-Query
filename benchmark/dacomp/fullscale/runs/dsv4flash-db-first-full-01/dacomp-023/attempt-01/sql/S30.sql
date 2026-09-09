WITH yearly AS (
  SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
  FROM "order" GROUP BY Category, yr
),
base AS (SELECT Category, sales AS s2015 FROM yearly WHERE yr=2015),
final AS (SELECT Category, sales AS s2018 FROM yearly WHERE yr=2018)
SELECT b.Category,
       ROUND(b.s2015, 2) AS sales_2015,
       ROUND(f.s2018, 2) AS sales_2018,
       ROUND(100.0 * (f.s2018 - b.s2015) / b.s2015, 2) AS total_growth_pct,
       ROUND(100.0 * (POWER(f.s2018 / b.s2015, 1.0/3.0) - 1), 2) AS cagr_pct
FROM base b JOIN final f USING (Category)
ORDER BY cagr_pct DESC