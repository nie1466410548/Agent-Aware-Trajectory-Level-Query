SELECT
 CASE
   WHEN c."Secincident Count" < 33 THEN 'Low (0-32)'
   WHEN c."Secincident Count" < 66 THEN 'Medium (33-65)'
   ELSE 'High (66-100)'
 END AS sec_group,
 e."Environmental Impact Rate", COUNT(*) n
FROM disaster_events d JOIN coordination_and_evaluation c ON c."Distribution Reference ID"=d."Disaster Event ID"
JOIN environment_and_health e ON e."Disaster Reference ID"=d."Disaster Event ID"
GROUP BY sec_group, e."Environmental Impact Rate" ORDER BY sec_group, e."Environmental Impact Rate"