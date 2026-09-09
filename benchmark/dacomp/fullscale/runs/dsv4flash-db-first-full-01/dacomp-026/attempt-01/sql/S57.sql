SELECT ba."Distribution Reference ID" AS ba_ref, de."Disaster Event ID" AS de_ref
FROM beneficiaries_and_assessments ba
JOIN disaster_events de ON ba."Distribution Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'
LIMIT 5