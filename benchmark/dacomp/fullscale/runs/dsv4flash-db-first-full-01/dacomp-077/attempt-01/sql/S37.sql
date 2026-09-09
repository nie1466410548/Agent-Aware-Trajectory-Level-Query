SELECT f.feature_id, f.feature_name, f.count_visitors, a.total_users_tried, a.regular_users, a.casual_users, a.avg_active_days_per_user
FROM pendo__feature f
JOIN pendo__product_adoption_analytics a ON a.feature_id = f.feature_id
WHERE f.count_visitors < 200
ORDER BY f.count_visitors DESC
LIMIT 47