SELECT SUBJECT, COUNT(*) AS n, MIN(strftime('%Y-%m-%d %H:%M', SENT_AT)) AS first_sent, MAX(strftime('%Y-%m-%d %H:%M', SENT_AT)) AS last_sent
FROM klaviyo__campaigns
GROUP BY SUBJECT
ORDER BY SUBJECT