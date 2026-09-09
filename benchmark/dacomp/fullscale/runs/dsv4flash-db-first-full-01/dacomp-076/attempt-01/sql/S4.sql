SELECT COUNT(*) AS total_customers,
       COUNT(DISTINCT profitability_segment) AS n_segments,
       COUNT(DISTINCT value_tier) AS n_tiers,
       COUNT(DISTINCT lifecycle_stage) AS n_lifecycle,
       COUNT(DISTINCT seasonal_preference) AS n_seasonal,
       COUNT(DISTINCT transaction_consistency) AS n_tx_consistency,
       COUNT(DISTINCT growth_potential) AS n_growth,
       COUNT(DISTINCT activity_status) AS n_activity,
       COUNT(DISTINCT retention_category) AS n_retention_cat,
       COUNT(DISTINCT recommended_action) AS n_rec_action,
       COUNT(DISTINCT engagement_frequency) AS n_engagement,
       COUNT(DISTINCT subsidiary_id) AS n_subsidiary
FROM netsuite2_customer_analytics