
WITH lang_stats AS (
  SELECT survey_id, user_language, COUNT(*) AS n, AVG(value) AS avg_v
  FROM qualtrics__response
  GROUP BY survey_id, user_language
  HAVING n >= 3
),
survey_stats AS (
  SELECT survey_id,
         MAX(avg_v) AS max_lang_avg,
         MIN(avg_v) AS min_lang_avg,
         SUM(n) AS total_resp,
         COUNT(*) AS n_langs
  FROM lang_stats
  GROUP BY survey_id
)
SELECT survey_id, max_lang_avg, min_lang_avg, total_resp, n_langs
FROM survey_stats
WHERE max_lang_avg > 7.0 AND min_lang_avg < 3.0
ORDER BY (max_lang_avg - min_lang_avg) DESC
LIMIT 30
