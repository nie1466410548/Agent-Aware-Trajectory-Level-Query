SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  COUNT(*) AS n,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.population.affected')),0) AS avg_affected,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.population.displaced')),0) AS avg_displaced,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.population.injured')),0) AS avg_injured,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.population.casualties')),0) AS avg_casualties,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.infrastructure.damage_percent')),1) AS avg_damage_pct,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.infrastructure.power_outage_percent')),1) AS avg_power_outage
FROM disaster_events de
GROUP BY severity