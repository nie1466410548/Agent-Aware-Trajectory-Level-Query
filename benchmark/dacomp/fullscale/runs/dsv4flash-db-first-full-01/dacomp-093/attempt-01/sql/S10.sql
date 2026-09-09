SELECT strftime('%w', SENT_AT) AS dow, COUNT(*) AS n,
       AVG(email_open_rate) AS avg_open, AVG(email_click_to_open_rate) AS avg_ctor
FROM klaviyo__campaigns
GROUP BY dow ORDER BY dow