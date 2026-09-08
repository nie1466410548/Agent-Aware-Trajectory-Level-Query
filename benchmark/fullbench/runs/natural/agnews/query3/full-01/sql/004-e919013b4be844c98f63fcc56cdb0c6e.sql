SELECT article_id, substr(publication_date,1,4) AS yr FROM article_metadata WHERE region='Europe' AND publication_date BETWEEN '2010-01-01' AND '2020-12-31'
