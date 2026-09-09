
SELECT c."Secincident Count", c."Accesslimitation", c."Safety Ranking",
       e."Disease Risk", e."Water Quality Index", e."Vaccination Coverage Rate",
       e."Sanitation Coverage Rate", e."Mental Health Assistance",
       d."Disaster Level"
FROM coordination_and_evaluation c
JOIN environment_and_health e ON e."Disaster Reference ID" = c."Distribution Reference ID"
JOIN disaster_events d ON d."Disaster Event ID" = c."Distribution Reference ID"
