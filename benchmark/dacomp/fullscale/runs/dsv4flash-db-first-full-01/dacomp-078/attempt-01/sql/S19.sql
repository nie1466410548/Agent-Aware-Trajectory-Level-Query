SELECT a.account_id, a.count_associated_visitors,
       a.count_active_days, a.count_active_months,
       a.sum_minutes, a.sum_events,
       a.average_daily_minutes, a.average_daily_events,
       a.avg_nps_rating,
       a.count_page_viewing_visitors, a.count_feature_clicking_visitors,
       a.last_event_on
FROM pendo__account a
LIMIT 10