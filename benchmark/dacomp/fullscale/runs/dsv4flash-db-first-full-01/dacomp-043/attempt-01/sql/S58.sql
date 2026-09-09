WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cm."Laboratory Tests (CBC/Antibody Test)" AS lab,
  cm."Imaging Studies (CT/X-ray)" AS imaging,
  cm."Medication & Dosage" AS med,
  cm."Allergic Reaction Management" AS allergy_mgmt,
  cm."Contact Management (Yes/No)" AS contact_mgmt,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, lab, imaging, med, allergy_mgmt, contact_mgmt
ORDER BY grp, n DESC;