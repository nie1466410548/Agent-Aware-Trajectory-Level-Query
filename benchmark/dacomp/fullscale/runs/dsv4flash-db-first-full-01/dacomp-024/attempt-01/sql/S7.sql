WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Order ID", s1."Customer ID",
         s2.Quantity, s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
),
agg AS (
  SELECT Region, Segment, COUNT(DISTINCT "Order ID") AS orders, COUNT(DISTINCT "Customer ID") AS customers,
         SUM(sales) AS sales, SUM(profit) AS profit
  FROM base GROUP BY Region, Segment
)
SELECT Region, Segment, orders, customers, ROUND(sales,0) AS sales, ROUND(profit,0) AS profit,
       ROUND(100.0*profit/sales,2) AS profit_margin_pct,
       ROUND(100.0*sales/SUM(sales) OVER (),2) AS sales_share_pct,
       ROUND(100.0*customers/SUM(customers) OVER (),2) AS customer_share_pct,
       ROUND(sales/orders,2) AS avg_order_value
FROM agg
ORDER BY sales DESC