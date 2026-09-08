SELECT "Symbol", "Financial Status", "Company Description"
FROM stockinfo
WHERE "Listing Exchange" = 'Q'
  AND "Financial Status" IN ('D','E','H');

