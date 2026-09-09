SELECT "Outcome (Cured/Improved/Deceased)" AS outcome, COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome;