SELECT COUNT(*) AS n_rows,
       MIN(created_at) AS min_created, MAX(created_at) AS max_created,
       MIN(updated_at) AS min_updated, MAX(updated_at) AS max_updated,
       COUNT(DISTINCT flow_id) AS n_flows,
       COUNT(DISTINCT variation_id) AS n_variations
FROM klaviyo__flows