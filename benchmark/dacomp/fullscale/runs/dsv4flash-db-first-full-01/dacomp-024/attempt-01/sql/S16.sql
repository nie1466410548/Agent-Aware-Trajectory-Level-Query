WITH base AS (
  SELECT s1.Region, substr(s1."Order Date", -4, 4) AS year, s2.Category, s2.Subcategory,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Category, ROUND(SUM(sales),0) AS sales, ROUND(SUM(profit),0) AS profit,
       ROUND(100.0*SUM(profit)/SUM(sales),2) AS margin_pct
FROM base GROUP BY Region, Category
ORDER BY Region, sales DESC