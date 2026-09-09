SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Number of Distribution Points",0)),0) AS affected_per_dist_point,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Daily Transport Volume (tons)",0)),0) AS affected_per_daily_ton,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.displaced') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.shelter.blankets'),0)),3) AS displaced_per_blanket,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.hygiene_kits'),0)),0) AS affected_per_hygiene_kit,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.essentials.water_liters'),0)),2) AS affected_per_liter_water
FROM disaster_events de
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
GROUP BY severity