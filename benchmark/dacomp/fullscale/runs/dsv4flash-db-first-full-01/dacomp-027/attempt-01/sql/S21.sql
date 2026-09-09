SELECT d."Disaster Level", e."Disease Risk", COUNT(*) n
FROM disaster_events d JOIN environment_and_health e ON e."Disaster Reference ID"=d."Disaster Event ID"
GROUP BY d."Disaster Level", e."Disease Risk" ORDER BY d."Disaster Level", e."Disease Risk"