SELECT "Patient_description", COUNT(*) AS n
FROM clinical_info
GROUP BY "Patient_description"
ORDER BY n DESC;
