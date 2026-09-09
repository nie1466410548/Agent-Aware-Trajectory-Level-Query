SELECT "Case ID", COUNT(*) AS n_records, COUNT(DISTINCT "Outcome (Cured/Improved/Deceased)") AS n_outcomes,
  GROUP_CONCAT(DISTINCT "Outcome (Cured/Improved/Deceased)") AS outcomes
FROM clinical_manifestations
GROUP BY "Case ID"
HAVING outcomes LIKE '%Deceased%'
ORDER BY n_records DESC;