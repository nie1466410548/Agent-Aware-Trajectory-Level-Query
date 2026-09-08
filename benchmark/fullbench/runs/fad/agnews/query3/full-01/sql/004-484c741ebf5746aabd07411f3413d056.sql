SELECT article_id, SUBSTR(publication_date,1,4) AS yr FROM article_metadata WHERE region='Europe' AND publication_date >= '2010-01-01' AND publication_date <= '2020-12-31'
