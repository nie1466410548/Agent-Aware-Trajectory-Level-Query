SELECT
 CASE
   WHEN c."Secincident Count" < 33 THEN 'Low (0-32)'
   WHEN c."Secincident Count" < 66 THEN 'Medium (33-65)'
   ELSE 'High (66-100)'
 END AS sec_group,
 COUNT(*) AS n,
 ROUND(AVG(e."Water Quality Index"),1) AS avg_wqi,
 ROUND(AVG(e."Sanitation Coverage Rate"),1) AS avg_sanitation,
 ROUND(AVG(e."Carbon Emissions (tons)"),1) AS avg_carbon,
 ROUND(AVG(e."Recycling Rate (%)"),1) AS avg_recycling,
 ROUND(AVG(e."Renewable Energy Share (%)"),1) AS avg_renewable,
 ROUND(AVG(e."Vaccination Coverage Rate"),1) AS avg_vaccination
FROM disaster_events d
JOIN coordination_and_evaluation c ON c."Distribution Reference ID" = d."Disaster Event ID"
JOIN environment_and_health e ON e."Disaster Reference ID" = d."Disaster Event ID"
GROUP BY sec_group
ORDER BY sec_group