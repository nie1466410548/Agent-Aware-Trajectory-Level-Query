SELECT gmap_id, AVG(rating) AS avg_rating, COUNT(*) AS review_count
FROM review
WHERE gmap_id IN ('gmap_22','gmap_25','gmap_33','gmap_24','gmap_20','gmap_21','gmap_28')
GROUP BY gmap_id
ORDER BY gmap_id

