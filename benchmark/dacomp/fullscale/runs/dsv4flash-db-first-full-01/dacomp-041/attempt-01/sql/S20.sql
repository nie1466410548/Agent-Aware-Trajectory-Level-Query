SELECT acm."Preserve Cultural Relic Reference", ar."Cultural Relic Reference Number"
FROM artifact_conservation_and_maint acm
LEFT JOIN artifact_rating ar ON TRIM(acm."Preserve Cultural Relic Reference") = TRIM(ar."Cultural Relic Reference Number")
WHERE ar."Cultural Relic Reference Number" IS NULL
LIMIT 5