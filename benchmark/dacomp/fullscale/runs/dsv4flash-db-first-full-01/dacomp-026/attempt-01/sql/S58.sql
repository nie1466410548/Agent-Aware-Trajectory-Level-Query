SELECT 
  ROUND(AVG(ba."Distribution Equity Index"),3) AS avg_equity,
  ROUND(AVG(ba."Affected Population Feedback Score"),2) AS avg_feedback,
  COUNT(*) AS n_ba,
  SUM(CASE WHEN ba."Needs Assessment Status"='Complete' THEN 1 ELSE 0 END) AS needs_complete,
  SUM(CASE WHEN ba."Vulnerability Assessment"='Complete' THEN 1 ELSE 0 END) AS vuln_complete
FROM beneficiaries_and_assessments ba
JOIN disaster_events de ON ba."Distribution Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'