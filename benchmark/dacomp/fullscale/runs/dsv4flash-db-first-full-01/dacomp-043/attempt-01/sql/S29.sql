
SELECT "PPE Usage" AS ppe, COUNT(*) AS n FROM isolation_and_disinfection GROUP BY ppe ORDER BY n DESC;