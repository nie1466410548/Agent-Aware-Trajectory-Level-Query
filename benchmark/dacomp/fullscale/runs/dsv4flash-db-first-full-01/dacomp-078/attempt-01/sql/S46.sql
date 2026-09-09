
SELECT 
  account_id, count_associated_visitors, avg_nps_rating,
  count_active_visitors, count_page_viewing_visitors, count_feature_clicking_visitors,
  count_active_days, count_active_months, sum_minutes, sum_events,
  average_daily_minutes, average_daily_events, first_event_on, last_event_on,
  CAST(count_active_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS active_visitor_ratio,
  CAST(count_page_viewing_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS page_view_ratio,
  CAST(count_feature_clicking_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS feature_click_ratio,
  CAST(sum_minutes AS REAL) / NULLIF(count_active_days, 0) AS minutes_per_active_day,
  CAST(sum_events AS REAL) / NULLIF(count_active_days, 0) AS events_per_active_day
FROM pendo__account ORDER BY account_id
