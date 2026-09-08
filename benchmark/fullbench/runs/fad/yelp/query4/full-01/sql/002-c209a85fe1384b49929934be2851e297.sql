SELECT business_ref, AVG(rating) AS avg_rating, COUNT(*) AS n_reviews FROM review GROUP BY business_ref
