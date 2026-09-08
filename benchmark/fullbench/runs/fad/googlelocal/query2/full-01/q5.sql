SELECT gmap_id, AVG(rating) AS avg_rating, COUNT(*) AS n
FROM review
WHERE gmap_id IN ('gmap_20','gmap_21','gmap_22','gmap_24','gmap_25','gmap_28','gmap_33')
GROUP BY gmap_id
