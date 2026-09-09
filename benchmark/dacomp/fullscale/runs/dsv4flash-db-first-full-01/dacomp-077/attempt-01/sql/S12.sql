SELECT f.feature_id, f.feature_name, f.count_visitors
FROM pendo__feature f
ORDER BY f.count_visitors ASC
LIMIT 20