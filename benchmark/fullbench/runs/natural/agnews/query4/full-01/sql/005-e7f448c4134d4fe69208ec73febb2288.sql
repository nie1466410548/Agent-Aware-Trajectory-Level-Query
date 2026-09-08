SELECT COUNT(*) AS total, SUM(CASE WHEN publication_date LIKE '2015%' THEN 1 ELSE 0 END) AS in2015 FROM article_metadata
