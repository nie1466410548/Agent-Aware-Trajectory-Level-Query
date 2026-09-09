SELECT p."Outlet Type",
  COUNT(DISTINCT s."Data Record ID") AS valid_sales_records,
  COUNT(DISTINCT c."Agreement ID") AS contracts,
  COUNT(DISTINCT cm."Management ID") AS mgmt_records,
  COUNT(DISTINCT a."Assessment ID") AS assessments
FROM "point_of_sale_(pos)_information" p
LEFT JOIN sales_data_table s ON p."Customer ID" = s."Customer ID" AND s."Data Status" = 'Valid'
LEFT JOIN contract_information_table c ON p."Outlet ID" = c."Outlet ID"
LEFT JOIN customer_management_table cm ON p."Customer ID" = cm."Customer ID"
LEFT JOIN assessment_result_table a ON p."Outlet ID" = a."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY p."Outlet Type"