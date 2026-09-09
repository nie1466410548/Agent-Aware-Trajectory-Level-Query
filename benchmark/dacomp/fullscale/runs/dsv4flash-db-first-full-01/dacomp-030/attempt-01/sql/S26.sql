SELECT p."Outlet Type",
  COUNT(cm."Management ID") AS mgmt_records,
  SUM(CASE WHEN cm." Warning Record" = 'Complaint Record' THEN 1 ELSE 0 END) AS complaint_cnt,
  SUM(CASE WHEN cm." Warning Record" = 'Quality Issue' THEN 1 ELSE 0 END) AS quality_cnt,
  ROUND(SUM(CASE WHEN cm." Warning Record" = 'Complaint Record' THEN 1 ELSE 0 END) * 1.0 / COUNT(cm."Management ID"), 3) AS complaint_ratio,
  SUM(CASE WHEN cm."Renewal Likelihood" = 'High' THEN 1 ELSE 0 END) AS renew_high,
  SUM(CASE WHEN cm."Renewal Likelihood" = 'Low' THEN 1 ELSE 0 END) AS renew_low,
  ROUND(AVG(cm."Training Count"), 2) AS avg_training
FROM "point_of_sale_(pos)_information" p
LEFT JOIN customer_management_table cm ON p."Customer ID" = cm."Customer ID"
GROUP BY p."Outlet Type"
ORDER BY complaint_ratio DESC