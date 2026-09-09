-- Check null columns in account table
SELECT COUNT(*) AS total,
  SUM(CASE WHEN min_nps_rating IS NULL THEN 1 ELSE 0 END) AS null_min_nps,
  SUM(CASE WHEN max_nps_rating IS NULL THEN 1 ELSE 0 END) AS null_max_nps,
  SUM(CASE WHEN avg_nps_rating IS NULL THEN 1 ELSE 0 END) AS null_avg_nps,
  SUM(CASE WHEN count_active_visitors IS NULL THEN 1 ELSE 0 END) AS null_active_vis,
  SUM(CASE WHEN count_page_viewing_visitors IS NULL THEN 1 ELSE 0 END) AS null_pv,
  SUM(CASE WHEN count_feature_clicking_visitors IS NULL THEN 1 ELSE 0 END) AS null_fc
FROM pendo__account