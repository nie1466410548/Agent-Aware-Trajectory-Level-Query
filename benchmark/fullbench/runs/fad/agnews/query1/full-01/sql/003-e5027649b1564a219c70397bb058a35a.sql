SELECT region, COUNT(*) AS n FROM article_metadata GROUP BY region ORDER BY n DESC;
