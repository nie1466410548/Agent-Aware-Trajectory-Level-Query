SELECT p."Outlet Type",
  COUNT(c."Agreement ID") AS num_contracts,
  COUNT(DISTINCT p."Outlet ID") AS num_outlets,
  ROUND(COUNT(c."Agreement ID") * 1.0 / COUNT(DISTINCT p."Outlet ID"), 2) AS contracts_per_outlet,
  ROUND(AVG(c."Signing Amount (CNY)"), 1) AS avg_signing_amount,
  ROUND(SUM(c."Signing Amount (CNY)"), 0) AS total_signing_amount,
  ROUND(AVG(c."Same-store Ratio"), 3) AS avg_same_store_ratio,
  SUM(CASE WHEN c."Renewal Flag" = 'Yes' THEN 1 ELSE 0 END) AS renewal_cnt,
  ROUND(AVG(CASE WHEN c."Renewal Flag" = 'Yes' THEN 1.0 ELSE 0 END), 3) AS renewal_ratio
FROM "point_of_sale_(pos)_information" p
LEFT JOIN contract_information_table c ON p."Outlet ID" = c."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY num_contracts DESC