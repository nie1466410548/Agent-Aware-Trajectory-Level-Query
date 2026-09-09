SELECT 
  COUNT(*) AS n,
  ROUND(AVG(json_extract("Staffing", '$.personnel.total')),1) AS avg_total_staff,
  ROUND(AVG(json_extract("Staffing", '$.personnel.medical')),1) AS avg_medical,
  ROUND(AVG(json_extract("Staffing", '$.personnel.security')),1) AS avg_security,
  ROUND(AVG(json_extract("Staffing", '$.personnel.logistics')),1) AS avg_logistics,
  ROUND(AVG(json_extract("Staffing", '$.personnel.volunteers')),1) AS avg_volunteers,
  ROUND(AVG(json_extract("Staffing", '$.readiness.availability_percent')),1) AS avg_availability,
  SUM(CASE WHEN json_extract("Staffing", '$.readiness.ppe_status')='Critical' THEN 1 ELSE 0 END) AS ppe_critical,
  SUM(CASE WHEN json_extract("Staffing", '$.readiness.ppe_status')='Adequate' THEN 1 ELSE 0 END) AS ppe_adequate,
  SUM(CASE WHEN json_extract("Staffing", '$.readiness.ppe_status')='Limited' THEN 1 ELSE 0 END) AS ppe_limited,
  SUM(CASE WHEN json_extract("Staffing", '$.readiness.training_status')='Complete' THEN 1 ELSE 0 END) AS training_complete
FROM human_resources hr JOIN disaster_events de ON de."Disaster Event ID" = hr."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'