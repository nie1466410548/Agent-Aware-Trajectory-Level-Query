WITH monthly AS (
  SELECT 
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Total Logistics Revenue") AS total_rev,
    SUM("Total Logistics Cost") AS total_cost,
    SUM("Freight Cost") AS freight,
    SUM("Warehousing Cost") AS warehousing,
    SUM("Other Operating Costs") AS other_cost,
    SUM("Logistics Value-Added Service Revenue") AS vas,
    SUM("Discount Amount") AS discount,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY month
)
SELECT 
  ROUND(AVG(total_profit),0) AS mean_profit,
  ROUND(MIN(total_profit),0) AS min_profit,
  ROUND(MAX(total_profit),0) AS max_profit,
  ROUND((MAX(total_profit)-MIN(total_profit))/AVG(total_profit)*100,1) AS range_pct_of_mean,
  ROUND(STDDEV(total_profit)/AVG(total_profit)*100,1) AS cv_profit_pct,
  ROUND(STDDEV(total_rev)/AVG(total_rev)*100,1) AS cv_rev_pct,
  ROUND(STDDEV(total_cost)/AVG(total_cost)*100,1) AS cv_cost_pct,
  ROUND(STDDEV(qty)/AVG(qty)*100,1) AS cv_qty_pct,
  ROUND(STDDEV(orders)/AVG(orders)*100,1) AS cv_orders_pct,
  ROUND(STDDEV(freight)/AVG(freight)*100,1) AS cv_freight_pct,
  ROUND(STDDEV(warehousing)/AVG(warehousing)*100,1) AS cv_warehousing_pct,
  ROUND(STDDEV(other_cost)/AVG(other_cost)*100,1) AS cv_othercost_pct,
  ROUND(STDDEV(vas)/AVG(vas)*100,1) AS cv_vas_pct,
  ROUND(STDDEV(discount)/AVG(discount)*100,1) AS cv_discount_pct
FROM monthly