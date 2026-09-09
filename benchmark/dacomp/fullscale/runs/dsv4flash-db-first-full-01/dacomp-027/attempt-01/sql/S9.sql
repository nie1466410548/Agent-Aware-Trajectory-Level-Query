SELECT d."Disaster Level", COUNT(*) AS n, ROUND(AVG(c."Secincident Count"),1) AS avg_sec, MIN(c."Secincident Count") AS min_sec, MAX(c."Secincident Count") AS max_sec
FROM disaster_events d JOIN coordination_and_evaluation c ON c."Distribution Reference ID" = d."Disaster Event ID"
GROUP BY d."Disaster Level"