
SELECT de."Disaster Event ID",
  ba."Distribution Equity Index" AS equity,
  ba."Affected Population Feedback Score" AS feedback
FROM disaster_events de
LEFT JOIN beneficiaries_and_assessments ba ON ba."Distribution Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'
