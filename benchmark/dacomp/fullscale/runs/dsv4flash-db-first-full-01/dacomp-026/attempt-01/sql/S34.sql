SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)),0) AS affected_per_staff,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(fin."budgetallot(USD)",0)),3) AS affected_per_1000usd,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.displaced') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.shelter.units'),0)),1) AS displaced_per_shelter_unit,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.essentials.food_tons'),0)),0) AS affected_per_food_ton,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.injured') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.medical'),0)),3) AS injured_per_medical_unit,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Total Transport Volume (tons)",0)),1) AS affected_per_transport_ton,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Number of Distribution Points",0)),0) AS affected_per_dist_point
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
GROUP BY severity