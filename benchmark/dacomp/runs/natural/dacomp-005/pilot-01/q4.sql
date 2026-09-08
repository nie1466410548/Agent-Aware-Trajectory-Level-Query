SELECT "Sales Quantity" AS qty, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low
FROM sheet1 GROUP BY qty ORDER BY qty
