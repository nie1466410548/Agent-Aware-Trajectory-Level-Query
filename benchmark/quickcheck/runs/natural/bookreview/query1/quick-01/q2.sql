SELECT
  COUNT(*) AS total,
  COUNT(substring(details from 'on [A-Z][a-z]+ \d{1,2}, (\d{4})')) AS with_year
FROM books_info;
