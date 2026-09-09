SELECT p."Outlet Type",
  COUNT(DISTINCT p."Customer ID") AS n_customers,
  ROUND(AVG(ci."Sales History"), 1) AS avg_sales_history,
  SUM(CASE WHEN ci."Customer Level" = 'A' THEN 1 ELSE 0 END) AS level_A,
  SUM(CASE WHEN ci."Customer Level" = 'B' THEN 1 ELSE 0 END) AS level_B,
  SUM(CASE WHEN ci."Customer Level" = 'C' THEN 1 ELSE 0 END) AS level_C,
  SUM(CASE WHEN ci."Customer Level" = 'D' THEN 1 ELSE 0 END) AS level_D
FROM "point_of_sale_(pos)_information" p
LEFT JOIN customer_information_table ci ON p."Customer ID" = ci."Customer ID"
GROUP BY p."Outlet Type"
ORDER BY n_customers DESC