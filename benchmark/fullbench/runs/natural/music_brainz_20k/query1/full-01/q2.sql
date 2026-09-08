SELECT store, SUM(units_sold) AS units, SUM(revenue_usd) AS revenue
FROM sales
WHERE track_id IN (4233, 12954, 15158)
  AND country = 'Canada'
  AND LOWER(store) LIKE '%apple%'
GROUP BY store;
