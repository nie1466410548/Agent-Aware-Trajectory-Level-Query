SELECT business_ref, COUNT(*) AS n_reviews, AVG(rating) AS avg_rating FROM review GROUP BY business_ref

