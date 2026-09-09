SELECT strftime('%Y', "Sales Date") AS yr, strftime('%m', "Sales Date") AS mo, COUNT(DISTINCT "Sales Date") AS days
FROM sales_records GROUP BY yr, mo ORDER BY yr, mo