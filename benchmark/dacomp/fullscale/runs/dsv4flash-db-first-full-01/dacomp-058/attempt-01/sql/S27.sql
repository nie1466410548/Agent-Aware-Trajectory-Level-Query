-- Get keyword-level data for avg_position
SELECT campaign_id, AVG(avg_position) AS avg_position FROM google_ads__keyword_report GROUP BY campaign_id