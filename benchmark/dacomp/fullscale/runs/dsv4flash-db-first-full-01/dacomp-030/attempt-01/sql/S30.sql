SELECT p."Outlet Type",
  c."Signing Type (GSB/Spark)" AS signing_type,
  COUNT(*) AS n_contracts,
  ROUND(AVG(c."Signing Amount (CNY)"), 1) AS avg_amt
FROM "point_of_sale_(pos)_information" p
JOIN contract_information_table c ON p."Outlet ID" = c."Outlet ID"
GROUP BY p."Outlet Type", signing_type
ORDER BY p."Outlet Type", signing_type