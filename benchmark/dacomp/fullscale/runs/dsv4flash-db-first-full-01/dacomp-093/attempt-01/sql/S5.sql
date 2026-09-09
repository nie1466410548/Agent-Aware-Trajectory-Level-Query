SELECT is_archived, variation_id IS NOT NULL AS has_variation, COUNT(*) AS n,
       COUNT(DISTINCT SUBJECT) AS n_subjects,
       AVG(email_open_rate) AS avg_open_rate,
       AVG(email_click_to_open_rate) AS avg_ctor,
       AVG(total_count_unique_people) AS avg_audience
FROM klaviyo__campaigns
GROUP BY 1,2