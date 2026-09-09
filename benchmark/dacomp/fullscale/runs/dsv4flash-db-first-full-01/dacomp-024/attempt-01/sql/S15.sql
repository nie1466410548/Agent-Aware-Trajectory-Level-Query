WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Customer ID" AS cid, s1."Order ID" AS oid,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
),
agg AS (
  SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
         COUNT(DISTINCT cid) AS customers, COUNT(DISTINCT oid) AS orders
  FROM base GROUP BY Region, Segment, year
)
SELECT Region, Segment, year, ROUND(sales,0) AS sales, ROUND(profit,0) AS profit,
       customers, orders,
       ROUND(100.0*sales/SUM(sales) OVER (PARTITION BY year),1) AS pct_of_year_sales,
       ROUND(100.0*customers/SUM(customers) OVER (PARTITION BY year),1) AS pct_of_year_customers,
       ROUND(100.0*profit/sales,2) AS margin_pct,
       ROUND(profit/customers,2) AS profit_per_customer,
       ROUND(sales/orders,2) AS avg_order_value
FROM agg
ORDER BY year, sales DESC