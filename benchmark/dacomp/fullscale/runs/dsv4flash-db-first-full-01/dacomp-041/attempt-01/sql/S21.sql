SELECT COUNT(*) as count
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
JOIN environmental_monitoring_data emd ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")
JOIN air_quality_readings aqr ON aqr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN light_and_radiation_readings lrr ON lrr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN surface_and_physical_readings spr ON spr."Environmental Monitoring Reference" = emd."Environmental Reading ID"
JOIN artifact_conservation_and_maint acm ON TRIM(acm."Gallery Reference") = TRIM(gi."Exhibition Hall Record ID")
JOIN artifact_rating ar ON TRIM(ar."Cultural Relic Reference Number") = TRIM(acm."Preserve Cultural Relic Reference")
JOIN basic_artifact_information bai ON TRIM(bai."Cultural Relic Registration Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN sensitivity_data sd ON TRIM(sd."Cultural Relic Reference Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN condition_assessment ca ON TRIM(ca."Inspected Cultural Relic Reference") = TRIM(ar."Cultural Relic Reference Number")
WHERE gi."Daily Visitor Count" > 900