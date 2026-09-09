
SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count",
       TRIM(acm."Preserve Cultural Relic Reference") as relic_ref,
       bai."Cultural Relic Name", bai."Dynasty", bai."Date (Year)", bai."Material Type", bai."Preservation Status",
       ar."Historical Significance Rating", ar."Research Value Rating", ar."Exhibition Value Rating",
       ar."Cultural Value Score", ar."Public Accessibility Rating", ar."Educational Value Rating",
       ar."Conservation Difficulty", ar."Treatment Complexity", ar."Material Stability", ar."Deterioration Rate",
       sd."Environmental Sensitivity", sd."Light Sensitivity", sd."Temperature Sensitivity", sd."Humidity Sensitivity",
       sd."Vibration Sensitivity", sd."Contamination Sensitivity",
       ca."Condition Assessment Rating",
       acm."Treatment Status", acm."Treatment Priority", acm."Treatment Effectiveness", acm."Reversibility Potential",
       sas." Security Level", sas."Insurance Value (USD)"
FROM gallery_information gi
JOIN artifact_conservation_and_maint acm ON TRIM(gi."Exhibition Hall Record ID") = TRIM(acm."Gallery Reference")
JOIN artifact_rating ar ON TRIM(ar."Cultural Relic Reference Number") = TRIM(acm."Preserve Cultural Relic Reference")
JOIN basic_artifact_information bai ON TRIM(bai."Cultural Relic Registration Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN sensitivity_data sd ON TRIM(sd."Cultural Relic Reference Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN condition_assessment ca ON TRIM(ca."Inspected Cultural Relic Reference") = TRIM(ar."Cultural Relic Reference Number")
JOIN artifact_security_and_access sas ON TRIM(sas."Cultural Relic Reference Number") = TRIM(ar."Cultural Relic Reference Number")
ORDER BY gi."Daily Visitor Count" DESC
