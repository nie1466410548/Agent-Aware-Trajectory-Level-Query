SELECT purchase_id, COUNT(*) AS num_reviews, AVG(rating) AS avg_rating
FROM review
GROUP BY purchase_id
HAVING AVG(rating) = 5.0

