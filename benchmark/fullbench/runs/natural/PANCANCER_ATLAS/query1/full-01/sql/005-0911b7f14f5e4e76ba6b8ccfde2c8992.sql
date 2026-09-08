SELECT histological_type, COUNT(*) FROM clinical_info WHERE "Patient_description" ILIKE '%lower grade glioma%' GROUP BY histological_type ORDER BY histological_type
