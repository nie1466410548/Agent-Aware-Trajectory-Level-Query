SELECT COUNT(*) AS total_managers,
  SUM(CASE WHEN total_requisitions_owned < 5 THEN 1 ELSE 0 END) AS excluded_low_req,
  SUM(CASE WHEN total_requisitions_owned >= 5 THEN 1 ELSE 0 END) AS eligible
FROM lever__hiring_manager_scorecard