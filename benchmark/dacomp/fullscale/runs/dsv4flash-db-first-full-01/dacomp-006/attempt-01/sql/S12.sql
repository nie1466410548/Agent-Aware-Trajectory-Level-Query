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
  ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit))/AVG(total_profit)*100,1) AS cv_profit_pct,
  ROUND(SQRT(AVG(total_rev*total_rev)-AVG(total_rev)*AVG(total_rev))/AVG(total_rev)*100,1) AS cv_rev_pct,
  ROUND(SQRT(AVG(total_cost*total_cost)-AVG(total_cost)*AVG(total_cost))/AVG(total_cost)*100,1) AS cv_cost_pct,
  ROUND(SQRT(AVG(qty*qty)-AVG(qty)*AVG(qty))/AVG(qty)*100,1) AS cv_qty_pct,
  ROUND(SQRT(AVG(orders*orders)-AVG(orders)*AVG(orders))/AVG(orders)*100,1) AS cv_orders_pct,
  ROUND(SQRT(AVG(freight*freight)-AVG(freight)*AVG(freight))/AVG(freight)*100,1) AS cv_freight_pct,
  ROUND(SQRT(AVG(warehousing*warehousing)-AVG(warehousing)*AVG(warehousing))/AVG(warehousing)*100,1) AS cv_warehousing_pct,
  ROUND(SQRT(AVG(other_cost*other_cost)-AVG(other_cost)*AVG(other_cost))/AVG(other_cost)*100,1) AS cv_othercost_pct,
  ROUND(SQRT(AVG(vas*vas)-AVG(vas)*AVG(vas))/AVG(vas)*100,1) AS cv_vas_pct,
  ROUND(SQRT(AVG(discount*discount)-AVG(discount)*AVG(discount))/AVG(discount)*100,1) AS cv_discount_pct
FROM monthly