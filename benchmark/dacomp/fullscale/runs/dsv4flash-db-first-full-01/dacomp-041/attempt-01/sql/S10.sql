SELECT emd."Display Case Reference", dci."Display case ID", dci."Gallery reference"
FROM environmental_monitoring_data emd
LEFT JOIN display_case_information dci ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")
WHERE dci."Display case ID" IS NULL
LIMIT 10