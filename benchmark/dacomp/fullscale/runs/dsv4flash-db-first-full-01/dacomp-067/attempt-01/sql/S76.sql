
SELECT scd.interview_name,
  AVG(scd.rating) as avg_rating,
  COUNT(*) as cnt,
  ROUND(SUM(CASE WHEN scd.rating >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as high_score_pct
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL AND scd.interview_name IS NOT NULL
GROUP BY scd.interview_name
ORDER BY avg_rating DESC
