
SELECT "Disaster Level",
 ROUND(AVG(json_extract("Impact Indicator",'$.infrastructure.damage_percent')),2) AS avg_damage_pct,
 ROUND(AVG(json_extract("Impact Indicator",'$.infrastructure.power_outage_percent')),2) AS avg_power_outage,
 ROUND(AVG(json_extract("Impact Indicator",'$.infrastructure.water_damage_percent')),2) AS avg_water_damage
FROM disaster_events GROUP BY "Disaster Level"
