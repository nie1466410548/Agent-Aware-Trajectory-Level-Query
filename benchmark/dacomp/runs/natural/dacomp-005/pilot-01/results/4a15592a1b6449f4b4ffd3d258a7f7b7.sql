SELECT COUNT(*) AS n_orders,
AVG("Profit Margin") AS avg_margin,
AVG("Profit Margin")*0.5 AS low_margin_threshold,
SUM(CASE WHEN "Profit Margin" < AVG("Profit Margin")*0.5 THEN 1 ELSE 0 END) AS dummy_check,
MIN("Profit Margin") AS min_margin, MAX("Profit Margin") AS max_margin,
MIN("Date") AS min_date, MAX("Date") AS max_date
FROM sheet1
