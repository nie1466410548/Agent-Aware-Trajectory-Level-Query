SELECT d."Disaster Level", e."Mental Health Assistance", COUNT(*) n
FROM disaster_events d JOIN environment_and_health e ON e."Disaster Reference ID"=d."Disaster Event ID"
GROUP BY d."Disaster Level", e."Mental Health Assistance" ORDER BY d."Disaster Level"