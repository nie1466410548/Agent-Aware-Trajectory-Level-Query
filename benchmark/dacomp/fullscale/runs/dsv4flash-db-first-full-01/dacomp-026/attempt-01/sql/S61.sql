
SELECT de."Disaster Severity Level",
  ROUND(AVG(ba."Distribution Equity Index"),3) AS avg_equity,
  ROUND(AVG(ba."Affected Population Feedback Score"),2) AS avg_feedback
FROM disaster_events de
LEFT JOIN beneficiaries_and_assessments ba ON ba."Distribution Reference ID" = de."Disaster Event ID"
GROUP BY de."Disaster Severity Level"
ORDER BY de."Disaster Severity Level"
