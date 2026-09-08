SELECT "Age Range" AS ar, "Customer Gender" AS g, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty,
ROUND(AVG("Profit Margin"),3) AS avg_margin
FROM sheet1 GROUP BY ar, g ORDER BY ar, g
