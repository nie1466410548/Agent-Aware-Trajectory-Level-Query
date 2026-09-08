SELECT
  count(*) AS total_lit_fiction,
  count(*) FILTER (WHERE details ILIKE '%english%') AS with_english,
  count(*) FILTER (WHERE details NOT ILIKE '%english%') AS without_english
FROM books_info
WHERE categories LIKE '%Literature & Fiction%'

