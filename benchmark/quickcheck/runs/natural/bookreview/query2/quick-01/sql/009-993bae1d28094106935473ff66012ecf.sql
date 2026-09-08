SELECT purchase_id, AVG(rating) AS avg_rating, COUNT(*) AS n_reviews, MIN(rating) AS min_r, MAX(rating) AS max_r FROM review GROUP BY purchase_id
