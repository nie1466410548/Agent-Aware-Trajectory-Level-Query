SELECT p."Outlet Type",
  COUNT(ph."Photo ID") AS n_photos,
  SUM(CASE WHEN ph."Review Status" = 'Failed' OR ph."Review Status" = 'Rejected' THEN 1 ELSE 0 END) AS failed_photos,
  ROUND(SUM(CASE WHEN ph."Review Status" = 'Failed' OR ph."Review Status" = 'Rejected' THEN 1 ELSE 0 END) * 1.0 / COUNT(ph."Photo ID"), 4) AS photo_fail_ratio
FROM "point_of_sale_(pos)_information" p
LEFT JOIN photo_information_table ph ON p."Outlet ID" = ph."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY photo_fail_ratio DESC