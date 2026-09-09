SELECT COUNT(DISTINCT campaign_id) AS n_camp, COUNT(*) AS n_rows, COUNT(DISTINCT source_relation) AS n_src
FROM klaviyo__campaigns