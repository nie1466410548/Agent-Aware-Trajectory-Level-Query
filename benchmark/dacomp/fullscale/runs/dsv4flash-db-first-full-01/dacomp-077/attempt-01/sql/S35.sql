SELECT feature_id, feature_name, total_users_tried, avg_events_per_user, avg_minutes_per_user, avg_active_days_per_user, regular_users, casual_users
FROM pendo__product_adoption_analytics
WHERE feature_id IN ('FEAT_00155','FEAT_00003','FEAT_00109','FEAT_00121','FEAT_00085','FEAT_00137','FEAT_00036','FEAT_00163')
ORDER BY total_users_tried DESC