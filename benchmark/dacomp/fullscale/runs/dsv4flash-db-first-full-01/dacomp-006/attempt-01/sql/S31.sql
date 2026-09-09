SELECT strftime('%Y-%m', "Date") AS month, COUNT(*) AS n,
  ROUND(AVG("Profit Margin"),3) AS avg_margin,
  ROUND(MIN("Profit Margin"),3) AS min_margin,
  ROUND(MAX("Profit Margin"),3) AS max_margin
FROM sheet1 WHERE "Destination" LIKE 'South China%'
GROUP BY month ORDER BY month