SELECT p."Outlet Type",
  COUNT(DISTINCT p."Outlet ID") AS num_outlets,
  -- Sales targets and actuals
  ROUND(AVG(p."Actual Sales (cases)"), 1) AS avg_actual_sales,
  ROUND(AVG(p."Sales Target"), 1) AS avg_sales_target,
  ROUND(SUM(p."Actual Sales (cases)") * 1.0 / NULLIF(SUM(p."Sales Target"), 0), 4) AS sales_target_achievement_pct,
  ROUND(AVG(p."VPO Value"), 2) AS avg_vpo,
  ROUND(AVG(p."PC Value"), 1) AS avg_pc_value,
  -- Sales data metrics
  ROUND(AVG(s." Target Achievement Rate"), 4) AS avg_target_achievement_rate,
  ROUND(AVG(s."Sales Volume (Units)"), 1) AS avg_sales_volume,
  ROUND(AVG(s."Sales (Value)"), 1) AS avg_sales_value,
  ROUND(SUM(s."Sales Volume (Units)"), 0) AS total_sales_volume,
  ROUND(SUM(s."Sales (Value)"), 0) AS total_sales_value,
  ROUND(AVG(s." YoY Growth Rate"), 2) AS avg_yoy_growth,
  ROUND(AVG(s."MoM Growth Rate"), 2) AS avg_mom_growth
FROM "point_of_sale_(pos)_information" p
LEFT JOIN sales_data_table s ON p."Customer ID" = s."Customer ID" AND s."Data Status" = 'Valid'
GROUP BY p."Outlet Type"
ORDER BY num_outlets DESC