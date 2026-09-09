-- Check distribution of count_associated_visitors, NPS, etc.
SELECT 
  MIN(count_associated_visitors) AS min_visitors,
  AVG(count_associated_visitors) AS avg_visitors,
  MAX(count_associated_visitors) AS max_visitors,
  MIN(count_active_visitors) AS min_active_vis,
  AVG(count_active_visitors) AS avg_active_vis,
  MAX(count_active_visitors) AS max_active_vis,
  MIN(count_page_viewing_visitors) AS min_pv,
  AVG(count_page_viewing_visitors) AS avg_pv,
  MAX(count_page_viewing_visitors) AS max_pv,
  MIN(count_feature_clicking_visitors) AS min_fc,
  AVG(count_feature_clicking_visitors) AS avg_fc,
  MAX(count_feature_clicking_visitors) AS max_fc
FROM pendo__account