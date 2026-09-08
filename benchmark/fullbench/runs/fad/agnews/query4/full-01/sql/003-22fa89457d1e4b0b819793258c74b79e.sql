SELECT region, COUNT(*) AS cnt FROM article_metadata GROUP BY region ORDER BY cnt DESC;

