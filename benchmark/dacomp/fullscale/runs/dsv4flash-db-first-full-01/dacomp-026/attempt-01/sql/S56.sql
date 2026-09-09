SELECT 
  ROUND(AVG("Distribution Equity Index"),3) AS avg_equity,
  ROUND(AVG("Affected Population Feedback Score"),2) AS avg_feedback,
  COUNT(*) AS n,
  SUM(CASE WHEN "Needs Assessment Status"='Complete' THEN 1 ELSE 0 END) AS needs_complete,
  SUM(CASE WHEN "Vulnerability Assessment"='Complete' THEN 1 ELSE 0 END) AS vuln_complete
FROM beneficiaries_and_assessments ba
WHERE "Distribution Reference ID" IN (SELECT "Disaster Event ID" FROM disaster_events WHERE "Disaster Severity Level"='Level 5')