SELECT gmap_id, COUNT(*) AS cnt
FROM review
WHERE rating >= 4.5 AND time LIKE '%2019%'
GROUP BY gmap_id
ORDER BY cnt DESC
LIMIT 20;
