SELECT (SELECT COUNT(*) FROM authors) AS n_authors,
       (SELECT MIN(publication_date) FROM article_metadata) AS min_date,
       (SELECT MAX(publication_date) FROM article_metadata) AS max_date,
       (SELECT COUNT(*) FROM article_metadata WHERE publication_date LIKE '2015%') AS n_2015;

