SELECT SUBJECT, COUNT(*) AS n, 
       AVG(email_open_rate) AS avg_open_rate,
       AVG(email_click_to_open_rate) AS avg_ctor,
       MIN(SUBJECT) AS sample_subject
FROM klaviyo__campaigns
GROUP BY SUBJECT
ORDER BY n DESC