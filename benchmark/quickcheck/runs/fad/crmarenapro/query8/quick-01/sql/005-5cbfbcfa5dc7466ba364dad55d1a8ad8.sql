SELECT COUNT(*) AS total_cases, MIN(createddate) AS min_d, MAX(createddate) AS max_d, COUNT(DISTINCT ownerid) AS distinct_owners
FROM "Case";

