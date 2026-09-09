WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s2.Quantity, s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
),
agg AS (
  SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
         COUNT(DISTINCT "Customer ID") AS customers
  FROM base GROUP BY Region, Segment, year
)
SELECT Region, Segment, year, sales, profit, customers,
       ROUND(100.0*(sales - LAG(sales) OVER (PARTITION BY Region, Segment ORDER BY year))/LAG(sales) OVER (PARTITION BY Region, Segment ORDER BY year),1) AS sales_yoy_pct,
       ROUND(100.0*(profit - LAG(profit) OVER (PARTITION BY Region, Segment ORDER BY year))/NULLIF(LAG(profit) OVER (PARTITION BY Region, Segment ORDER BY year),0),1) AS profit_yoy_pct
FROM agg ORDER BY Region, Segment, year