SELECT n_langs_in_resp, COUNT(*) AS n_users
FROM (
  SELECT recipient_email, COUNT(DISTINCT user_language) AS n_langs_in_resp
  FROM qualtrics__response
  GROUP BY recipient_email
) t
GROUP BY n_langs_in_resp
ORDER BY n_langs_in_resp