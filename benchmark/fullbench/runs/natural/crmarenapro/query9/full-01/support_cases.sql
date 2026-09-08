SELECT id, accountid, status, priority, createddate, closeddate
FROM "Case"
WHERE createddate >= '2021-01-01'
ORDER BY createddate;
