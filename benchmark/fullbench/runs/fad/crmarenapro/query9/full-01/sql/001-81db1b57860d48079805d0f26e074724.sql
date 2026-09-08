SELECT id, accountid, createddate, closeddate, status
FROM "Case"
WHERE closeddate IS NOT NULL
  AND createddate >= '2021-04-01'
  AND createddate < '2022-10-01';

