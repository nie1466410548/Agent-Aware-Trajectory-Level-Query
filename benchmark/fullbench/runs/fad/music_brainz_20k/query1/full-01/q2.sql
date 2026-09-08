SELECT track_id, country, store, units_sold, revenue_usd
FROM sales
WHERE track_id IN (4233, 12954, 15158)
  AND country = 'Canada'
  AND LOWER(store) LIKE '%apple%';
