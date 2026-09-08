SELECT gmap_id, AVG(rating) AS avg_rating, COUNT(*) AS n_reviews FROM review GROUP BY gmap_id
