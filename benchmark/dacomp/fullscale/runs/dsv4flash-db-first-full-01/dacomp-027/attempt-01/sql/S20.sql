SELECT d."Disaster Level", e."Environmental Impact Rate", COUNT(*) n
FROM disaster_events d JOIN environment_and_health e ON e."Disaster Reference ID"=d."Disaster Event ID"
GROUP BY d."Disaster Level", e."Environmental Impact Rate" ORDER BY d."Disaster Level", e."Environmental Impact Rate"