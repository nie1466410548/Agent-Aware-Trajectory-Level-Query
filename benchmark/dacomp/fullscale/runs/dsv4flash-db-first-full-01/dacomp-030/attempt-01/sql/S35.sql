SELECT p."Outlet Type",
  ROUND(AVG(d."Number of failures"), 2) AS avg_failures,
  COUNT(d."Equipment record code") AS n_devices
FROM "point_of_sale_(pos)_information" p
LEFT JOIN device_information_table d ON p."Outlet ID" = d."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY avg_failures DESC