SELECT 
  COUNT(*) AS n,
  ROUND(AVG(json_extract("Inventory resources", '$.power.generators')),1) AS avg_generators,
  ROUND(AVG(json_extract("Inventory resources", '$.power.fuel_liters')),0) AS avg_fuel,
  ROUND(AVG(json_extract("Inventory resources", '$.medical')),0) AS avg_medical,
  ROUND(AVG(json_extract("Inventory resources", '$.shelter.units')),0) AS avg_shelter,
  ROUND(AVG(json_extract("Inventory resources", '$.shelter.blankets')),0) AS avg_blankets,
  ROUND(AVG(json_extract("Inventory resources", '$.essentials.food_tons')),1) AS avg_food,
  ROUND(AVG(json_extract("Inventory resources", '$.essentials.water_liters')),0) AS avg_water,
  ROUND(AVG(json_extract("Inventory resources", '$.hygiene_kits')),0) AS avg_hygiene
FROM supplies1 sup JOIN disaster_events de ON de."Disaster Event ID" = sup."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'