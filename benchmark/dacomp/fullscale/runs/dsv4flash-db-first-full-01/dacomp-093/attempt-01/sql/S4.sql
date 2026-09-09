SELECT COUNT(*) AS n_campaigns,
       COUNT(DISTINCT campaign_id) AS n_campaign_ids,
       COUNT(DISTINCT variation_id) AS n_variations,
       MIN(SENT_AT) AS min_sent, MAX(SENT_AT) AS max_sent,
       COUNT(*) FILTER (WHERE SENT_AT IS NULL) AS null_sent
FROM klaviyo__campaigns