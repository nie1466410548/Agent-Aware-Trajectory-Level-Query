SELECT p."Outlet Type",
  COUNT(d."Equipment record code") AS n_devices,
  SUM(d."Number of failures") AS total_failures,
  ROUND(AVG(d."Number of failures"), 2) AS avg_failures
FROM "point_of_sale_(pos)_information" p
LEFT JOIN device_information_table d ON p."Outlet ID" = d."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY avg_failures DESC