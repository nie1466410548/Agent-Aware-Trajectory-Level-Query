SELECT COUNT(*) AS n_reviews, COUNT(DISTINCT purchase_id) AS n_books_rated, AVG(rating) AS avg_rating FROM review
