
SELECT interview_name,
  COUNT(*) as total,
  ROUND(SUM(CASE WHEN lower(overall_recommendation) IN ('strong_yes','yes') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as positive_pct,
  AVG(duration_interview_minutes) as avg_duration
FROM greenhouse__interview_enhanced
WHERE overall_recommendation IS NOT NULL
GROUP BY interview_name
ORDER BY total DESC
