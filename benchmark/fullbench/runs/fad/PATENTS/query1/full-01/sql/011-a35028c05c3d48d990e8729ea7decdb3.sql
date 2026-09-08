WITH exploded AS (
  SELECT DISTINCT p.rowid AS rid,
         UPPER(SUBSTR(TRIM(json_extract(je.value, '$.code')), 1, 4)) AS subclass,
         CASE
           WHEN TRIM(p.filing_date) GLOB '*[0-9][0-9][0-9][0-9]' THEN CAST(SUBSTR(TRIM(p.filing_date), -4) AS INTEGER)
           WHEN TRIM(p.filing_date) GLOB '[0-9][0-9][0-9][0-9]*' THEN CAST(SUBSTR(TRIM(p.filing_date), 1, 4) AS INTEGER)
           ELSE NULL
         END AS yr
  FROM publicationinfo p, json_each(p.cpc) je
)
SELECT subclass, yr, COUNT(*) AS n
FROM exploded
WHERE yr IS NOT NULL AND subclass IS NOT NULL AND subclass <> ''
GROUP BY subclass, yr
ORDER BY subclass, yr;

