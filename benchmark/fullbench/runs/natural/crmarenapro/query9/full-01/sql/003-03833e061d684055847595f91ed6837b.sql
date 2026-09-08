SELECT
  MIN(createddate) AS min_created,
  MAX(createddate) AS max_created,
  MIN(closeddate) AS min_closed,
  MAX(closeddate) AS max_closed,
  COUNT(*) AS total_cases,
  COUNT(closeddate) AS closed_cases
FROM "Case";

