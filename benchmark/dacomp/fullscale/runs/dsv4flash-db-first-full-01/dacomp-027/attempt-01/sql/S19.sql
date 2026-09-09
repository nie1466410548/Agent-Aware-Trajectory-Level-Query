SELECT
 CASE
   WHEN c."Secincident Count" < 33 THEN 'Low (0-32)'
   WHEN c."Secincident Count" < 66 THEN 'Medium (33-65)'
   ELSE 'High (66-100)'
 END AS sec_group,
 COUNT(*) AS n,
 ROUND(AVG(json_extract(d."Impact Indicator",'$.population.affected')),0) AS avg_affected,
 ROUND(AVG(json_extract(d."Impact Indicator",'$.population.displaced')),0) AS avg_displaced,
 ROUND(AVG(json_extract(d."Impact Indicator",'$.population.casualties')),0) AS avg_casualties,
 ROUND(AVG(json_extract(d."Impact Indicator",'$.infrastructure.damage_percent')),1) AS avg_damage_pct,
 ROUND(AVG(json_extract(d."Impact Indicator",'$.infrastructure.power_outage_percent')),1) AS avg_power_outage
FROM disaster_events d
JOIN coordination_and_evaluation c ON c."Distribution Reference ID" = d."Disaster Event ID"
GROUP BY sec_group
ORDER BY sec_group