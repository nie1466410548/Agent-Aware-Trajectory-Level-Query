SELECT 
  COUNT(*) AS n,
  ROUND(AVG("partnerorgs"),1) AS avg_partner_orgs,
  ROUND(AVG("reportcompliance"),1) AS avg_report_compliance,
  ROUND(AVG("dataqualityvalue"),0) AS avg_data_quality,
  ROUND(AVG("stakeholdersatisf"),1) AS avg_stakeholder_satisf,
  ROUND(AVG("publicperception"),1) AS avg_public_perception,
  ROUND(AVG("Secincident Count"),0) AS avg_sec_incidents,
  SUM(CASE WHEN "compliancestate"='Compliant' THEN 1 ELSE 0 END) AS compliant,
  SUM(CASE WHEN "auditstate"='Passed' THEN 1 ELSE 0 END) AS audit_passed,
  SUM(CASE WHEN "lessonsrecorded">0 THEN 1 ELSE 0 END) AS has_lessons,
  SUM(CASE WHEN "bestpracticeslisted">0 THEN 1 ELSE 0 END) AS has_best_practices,
  SUM(CASE WHEN "improvementrecs">0 THEN 1 ELSE 0 END) AS has_improvements
FROM coordination_and_evaluation ce JOIN disaster_events de ON de."Disaster Event ID"=ce."Action Reference ID"
WHERE de."Disaster Severity Level"='Level 5'