SELECT purchase_id, AVG(rating) AS avg_rating, COUNT(*) AS n_reviews FROM review WHERE review_time >= '2020-01-01' GROUP BY purchase_id
