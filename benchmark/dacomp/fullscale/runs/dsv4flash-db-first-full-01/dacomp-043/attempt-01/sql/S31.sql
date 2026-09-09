SELECT "Initial Diagnosis (Suspected/Clinical/Confirmed)" AS init_diag,
  "Diagnostic Quality Score" AS quality,
  "Diagnostic Criteria Compliance Rate" AS compliance,
  COUNT(*) AS n
FROM diagnosis_and_classification
GROUP BY init_diag, quality, compliance
ORDER BY n DESC
LIMIT 20;