SELECT p."Outlet Type",
  ROUND(MIN(s." Target Achievement Rate"), 4) AS min_tar,
  ROUND(AVG(s." Target Achievement Rate"), 4) AS avg_tar,
  ROUND(MAX(s." Target Achievement Rate"), 4) AS max_tar,
  ROUND(AVG(s."Sales (Value)"), 1) AS avg_sales_value,
  ROUND(COUNT(s."Data Record ID"), 0) AS n
FROM "point_of_sale_(pos)_information" p
JOIN sales_data_table s ON p."Customer ID" = s."Customer ID" AND s."Data Status" = 'Valid'
GROUP BY p."Outlet Type"
ORDER BY avg_tar DESC