SELECT COUNT(*) AS n, SUM(CASE WHEN first_click_at IS NOT NULL THEN 1 ELSE 0 END) AS has_first_click,
  SUM(CASE WHEN last_click_at IS NOT NULL THEN 1 ELSE 0 END) AS has_last_click
FROM pendo__visitor_feature