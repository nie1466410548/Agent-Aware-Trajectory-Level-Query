SELECT filing_date, COUNT(*) AS n
FROM publicationinfo
WHERE NOT (TRIM(filing_date) GLOB '*[0-9][0-9][0-9][0-9]')
GROUP BY filing_date
ORDER BY n DESC
LIMIT 30;
