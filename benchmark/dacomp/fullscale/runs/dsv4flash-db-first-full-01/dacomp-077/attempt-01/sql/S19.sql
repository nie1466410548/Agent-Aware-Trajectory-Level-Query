SELECT f.feature_id, f.feature_name, f.count_visitors, f.is_core_event, f.product_area_name
FROM pendo__feature f
WHERE f.count_visitors < 200
ORDER BY f.count_visitors DESC