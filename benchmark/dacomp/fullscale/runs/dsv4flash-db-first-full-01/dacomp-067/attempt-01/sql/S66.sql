
SELECT attribute_name, 
  COUNT(*) as cnt,
  AVG(rating) as avg_rating
FROM greenhouse__interview_scorecard_detail
WHERE attribute_name IS NOT NULL AND rating IS NOT NULL
GROUP BY attribute_name
ORDER BY avg_rating DESC
