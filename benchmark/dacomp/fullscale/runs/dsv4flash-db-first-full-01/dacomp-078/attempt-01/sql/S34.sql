SELECT f.feature_id, f.feature_name, f.page_name, f.app_display_name, f.app_platform, f.is_core_event,
       f.count_visitors, f.count_accounts, f.sum_clicks
FROM pendo__feature f
LIMIT 8