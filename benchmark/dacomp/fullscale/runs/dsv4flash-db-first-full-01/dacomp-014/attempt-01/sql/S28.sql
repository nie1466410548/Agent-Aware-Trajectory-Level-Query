SELECT 
  "Creator Video Count",
  COUNT(*) as cnt,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Creator Video Count"
HAVING cnt >= 10
ORDER BY "Creator Video Count"