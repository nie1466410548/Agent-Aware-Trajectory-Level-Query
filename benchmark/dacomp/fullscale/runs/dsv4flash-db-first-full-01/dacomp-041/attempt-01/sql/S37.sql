
SELECT ur.* FROM usage_records ur
JOIN artifact_conservation_and_maint acm ON TRIM(acm."Preserve Cultural Relic Reference") = TRIM(ur."Cultural Relic Reference Number")
JOIN gallery_information gi ON TRIM(gi."Exhibition Hall Record ID") = TRIM(acm."Gallery Reference")
WHERE gi."Daily Visitor Count" > 900
