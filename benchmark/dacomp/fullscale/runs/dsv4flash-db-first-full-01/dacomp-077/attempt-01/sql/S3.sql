SELECT
 (SELECT COUNT(*) FROM pendo__feature) AS n_features,
 (SELECT COUNT(*) FROM pendo__visitor) AS n_visitors,
 (SELECT COUNT(*) FROM pendo__visitor_feature) AS n_visitor_feature,
 (SELECT COUNT(*) FROM pendo__feature_daily_metrics) AS n_feature_daily,
 (SELECT COUNT(*) FROM pendo__customer_lifecycle_insights) AS n_clv,
 (SELECT COUNT(*) FROM pendo__product_adoption_analytics) AS n_adoption,
 (SELECT COUNT(*) FROM pendo__account) AS n_accounts