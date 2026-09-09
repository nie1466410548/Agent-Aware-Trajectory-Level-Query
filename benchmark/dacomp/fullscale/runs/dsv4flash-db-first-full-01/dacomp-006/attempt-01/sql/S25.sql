WITH rev_month AS (
  SELECT strftime('%Y-%m',"Date") AS month,
    SUM("Total Logistics Revenue") AS rev,
    SUM("List Price Revenue") AS list_price,
    SUM("Logistics Value-Added Service Revenue") AS vas,
    SUM("Discount Amount") AS discount,
    SUM("Total Logistics Cost") AS cost,
    SUM("Freight Cost") AS freight,
    SUM("Warehousing Cost") AS warehousing,
    SUM("Other Operating Costs") AS other_cost,
    SUM("Profit") AS profit
  FROM sheet1 WHERE "Destination" LIKE 'South China%'
  GROUP BY 1
)
SELECT month, ROUND(rev,0) AS rev, ROUND(profit,0) AS profit, ROUND(cost,0) AS cost,
  ROUND(discount,0) AS discount, ROUND(freight,0) AS freight, ROUND(warehousing,0) AS warehousing,
  ROUND(other_cost,0) AS other_cost, ROUND(vas,0) AS vas
FROM rev_month ORDER BY month