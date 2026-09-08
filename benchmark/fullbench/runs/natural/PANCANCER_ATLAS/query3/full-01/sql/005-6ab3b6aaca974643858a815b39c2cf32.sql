SELECT histological_type, COUNT(*) AS n FROM clinical_info WHERE "Patient_description" ILIKE '%Breast invasive carcinoma%' GROUP BY histological_type ORDER BY n DESC
