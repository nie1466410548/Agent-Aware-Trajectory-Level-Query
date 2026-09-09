SELECT 
  COUNT(*) AS n,
  ROUND(AVG(ce."partnerorgs"),1) AS avg_partner_orgs,
  ROUND(AVG(ce."reportcompliance"),1) AS avg_report_compliance,
  ROUND(AVG(ce."dataqualityvalue"),0) AS avg_data_quality,
  ROUND(AVG(ce."stakeholdersatisf"),1) AS avg_stakeholder_satisf,
  ROUND(AVG(ce."publicperception"),1) AS avg_public_perception,
  ROUND(AVG(ce."Secincident Count"),0) AS avg_sec_incidents,
  SUM(CASE WHEN ce."compliancestate"='Compliant' THEN 1 ELSE 0 END) AS compliant,
  SUM(CASE WHEN ce."auditstate"='Passed' THEN 1 ELSE 0 END) AS audit_passed,
  ROUND(AVG(ce."lessonsrecorded"),0) AS avg_lessons,
  ROUND(AVG(ce."bestpracticeslisted"),0) AS avg_best_practices,
  ROUND(AVG(ce."improvementrecs"),0) AS avg_improvements
FROM coordination_and_evaluation ce
JOIN operations1 op ON op."Operation ID" = ce."Action Reference ID"
JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'