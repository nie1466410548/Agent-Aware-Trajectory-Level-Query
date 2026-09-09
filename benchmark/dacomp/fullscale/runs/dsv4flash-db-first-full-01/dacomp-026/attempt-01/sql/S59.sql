SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  ROUND(AVG(json_extract(sup."Inventory resources", '$.power.generators')),1) AS avg_gen,
  ROUND(AVG(json_extract(sup."Inventory resources", '$.medical')),0) AS avg_med,
  ROUND(AVG(json_extract(sup."Inventory resources", '$.shelter.units')),0) AS avg_shelter,
  ROUND(AVG(json_extract(sup."Inventory resources", '$.essentials.food_tons')),1) AS avg_food,
  ROUND(AVG(json_extract(sup."Inventory resources", '$.essentials.water_liters')),0) AS avg_water,
  ROUND(AVG(tr."Total Transport Volume (tons)"),0) AS avg_transport_vol,
  ROUND(AVG(tr."Daily Transport Volume (tons)"),0) AS avg_daily_vol,
  ROUND(AVG(tr."Number of Vehicles"),1) AS avg_vehicles,
  ROUND(AVG(tr."Number of Distribution Points"),0) AS avg_dist_points,
  ROUND(AVG(tr."Average Delivery Time"),1) AS avg_deliv_time,
  ROUND(AVG(tr."Delivery Success Rate"),1) AS avg_deliv_success,
  ROUND(AVG(tr."Vehicle Failure Rate"),1) AS avg_failure_rate
FROM disaster_events de
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
GROUP BY severity