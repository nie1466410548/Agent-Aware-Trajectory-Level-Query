SELECT purchase_id, AVG(rating) AS avg_rating, COUNT(*) AS n_reviews FROM review GROUP BY purchase_id
