SELECT gi."Exhibition Hall Record ID", dci."Gallery reference"
FROM gallery_information gi
LEFT JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
WHERE dci."Gallery reference" IS NULL
LIMIT 5