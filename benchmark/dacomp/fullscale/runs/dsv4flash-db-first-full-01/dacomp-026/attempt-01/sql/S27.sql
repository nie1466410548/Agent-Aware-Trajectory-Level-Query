SELECT 
  COUNT(*) AS n,
  ROUND(AVG("Number of Vehicles"),1) AS avg_vehicles,
  ROUND(AVG("Available Trucks"),1) AS avg_trucks,
  ROUND(AVG("Available Helicopters"),1) AS avg_helis,
  ROUND(AVG("Available Ships"),1) AS avg_ships,
  ROUND(AVG("Total Transport Volume (tons)"),0) AS avg_total_vol,
  ROUND(AVG("Daily Transport Volume (tons)"),0) AS avg_daily_vol,
  ROUND(AVG("Number of Distribution Points"),0) AS avg_dist_points,
  ROUND(AVG("Average Delivery Time"),1) AS avg_deliv_time,
  ROUND(AVG("Delivery Success Rate"),1) AS avg_deliv_success,
  ROUND(AVG("Fuel Consumption (L/km)"),1) AS avg_fuel,
  ROUND(AVG("Vehicle Failure Rate"),1) AS avg_fail_rate,
  SUM(CASE WHEN "Last-Mile Delivery Status"='On Track' THEN 1 ELSE 0 END) AS lm_ontrack,
  SUM(CASE WHEN "Last-Mile Delivery Status"='Delayed' THEN 1 ELSE 0 END) AS lm_delayed,
  SUM(CASE WHEN "Route Optimization Status"='Optimized' THEN 1 ELSE 0 END) AS route_opt,
  SUM(CASE WHEN "Maintenance Status"='Up to Date' THEN 1 ELSE 0 END) AS maint_ok
FROM transportation1 tr JOIN disaster_events de ON de."Disaster Event ID" = tr."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'