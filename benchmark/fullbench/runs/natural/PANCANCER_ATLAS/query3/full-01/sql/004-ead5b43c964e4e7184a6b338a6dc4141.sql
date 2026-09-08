SELECT patient_id, tissue_source_site, histological_type, "Patient_description" FROM clinical_info WHERE "Patient_description" ILIKE '%breast%' LIMIT 6
