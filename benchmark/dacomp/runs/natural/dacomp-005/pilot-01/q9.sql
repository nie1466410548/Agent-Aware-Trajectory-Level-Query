SELECT STRFTIME('%Y-%m',"Date") AS ym, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Profit Margin"),3) AS avg_margin,
ROUND(AVG("Discount Amount"/"List Price Revenue")*100,2) AS avg_disc_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty
FROM sheet1 GROUP BY ym ORDER BY ym
