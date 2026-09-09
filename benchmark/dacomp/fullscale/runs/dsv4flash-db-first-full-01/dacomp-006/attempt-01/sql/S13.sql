WITH monthly AS (
  SELECT 
    "Consigned Product" AS dim,
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Sales Quantity") AS qty
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY "Consigned Product", month
),
stats AS (
  SELECT dim,
    ROUND(AVG(total_profit),0) AS mean_profit,
    ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit)),0) AS sd_profit,
    ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit))/AVG(total_profit)*100,1) AS cv_pct,
    ROUND(SUM(total_profit),0) AS annual_profit,
    ROUND(SUM(total_profit) * 100.0 / (SELECT SUM("Profit") FROM sheet1 WHERE "Destination" LIKE 'South China%'),1) AS pct_of_total
  FROM monthly
  GROUP BY dim
)
SELECT * FROM stats ORDER BY cv_pct DESC