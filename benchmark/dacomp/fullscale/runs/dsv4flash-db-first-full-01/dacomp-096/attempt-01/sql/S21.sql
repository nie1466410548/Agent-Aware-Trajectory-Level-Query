SELECT COUNT(*) AS n_persons,
       COUNT(DISTINCT last_touch_flow_id) AS n_flows_touched,
       COUNT(DISTINCT last_touch_campaign_id) AS n_camps_touched,
       COUNT(DISTINCT variation_id) AS n_variations,
       MIN(last_event_at) AS min_last_event, MAX(last_event_at) AS max_last_event,
       SUM(has_converted) AS n_converted
FROM klaviyo__person_campaign_flow