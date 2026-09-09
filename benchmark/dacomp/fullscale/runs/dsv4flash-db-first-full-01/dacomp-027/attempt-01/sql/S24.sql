SELECT d."Disaster Level", c."evaluationstage", COUNT(*) n
FROM disaster_events d JOIN coordination_and_evaluation c ON c."Distribution Reference ID"=d."Disaster Event ID"
GROUP BY d."Disaster Level", c."evaluationstage" ORDER BY d."Disaster Level", n DESC