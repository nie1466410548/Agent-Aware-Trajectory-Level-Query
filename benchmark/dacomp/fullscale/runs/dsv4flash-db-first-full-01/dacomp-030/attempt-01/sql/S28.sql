SELECT p."Outlet Type",
  COUNT(ap."Appeal ID") AS n_appeals,
  SUM(CASE WHEN ap."Handling Status" = 'Completed' THEN 1 ELSE 0 END) AS completed_appeals,
  SUM(CASE WHEN ap."Processing Result" = 'Modify score' THEN 1 ELSE 0 END) AS modified_scores,
  ROUND(COUNT(ap."Appeal ID") * 1.0 / COUNT(DISTINCT p."Outlet ID"), 2) AS appeals_per_outlet
FROM "point_of_sale_(pos)_information" p
LEFT JOIN appeal_record_table ap ON p."Outlet ID" = ap."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY n_appeals DESC