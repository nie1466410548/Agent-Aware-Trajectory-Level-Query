SELECT variation_id, COUNT(*) AS n, AVG(email_open_rate) AS avg_open_rate, AVG(email_click_to_open_rate) AS avg_ctor
FROM klaviyo__campaigns
GROUP BY variation_id