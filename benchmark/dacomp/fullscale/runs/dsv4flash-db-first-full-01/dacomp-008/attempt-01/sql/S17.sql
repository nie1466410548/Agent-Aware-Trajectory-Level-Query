SELECT
  "Project Type",
  ROUND(AVG(CASE WHEN "Project Status" = 'Completed' THEN "Budget Amount" - "Actual Cost" END), 2) as completed_avg_dev,
  COUNT(CASE WHEN "Project Status" = 'Completed' THEN 1 END) as completed_n,
  ROUND(AVG(CASE WHEN "Project Status" = 'In Progress' THEN "Budget Amount" - "Actual Cost" END), 2) as inprogress_avg_dev,
  COUNT(CASE WHEN "Project Status" = 'In Progress' THEN 1 END) as inprogress_n,
  ROUND(AVG(CASE WHEN "Project Status" = 'Delayed' THEN "Budget Amount" - "Actual Cost" END), 2) as delayed_avg_dev,
  COUNT(CASE WHEN "Project Status" = 'Delayed' THEN 1 END) as delayed_n
FROM sheet1
GROUP BY "Project Type"
ORDER BY "Project Type"