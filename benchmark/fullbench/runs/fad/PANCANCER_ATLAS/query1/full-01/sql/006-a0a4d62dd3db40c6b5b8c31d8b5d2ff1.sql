SELECT patient_id, histological_type FROM clinical_info WHERE "Patient_description" ILIKE '%lower grade glioma%' AND histological_type IS NOT NULL AND histological_type NOT LIKE '[%'
