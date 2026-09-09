
SELECT "Symptom Monitoring During Isolation" AS monitor, COUNT(*) AS n FROM isolation_and_disinfection GROUP BY monitor ORDER BY n DESC;