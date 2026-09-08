SELECT patient_id, histological_type
FROM clinical_info
WHERE "Patient_description" ILIKE '%Breast invasive carcinoma%'
  AND "Patient_description" ILIKE '%FEMALE%'
  AND histological_type IS NOT NULL;
