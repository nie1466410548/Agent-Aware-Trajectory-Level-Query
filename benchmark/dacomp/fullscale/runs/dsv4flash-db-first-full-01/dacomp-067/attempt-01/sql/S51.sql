SELECT attribute_name, 
       COUNT(*) as cnt,
       AVG(rating) as avg_rating,
       ROUND(SUM(CASE WHEN rating >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as high_score_pct
FROM greenhouse__interview_scorecard_detail
WHERE attribute_name IS NOT NULL AND rating IS NOT NULL
GROUP BY attribute_name
ORDER BY avg_rating DESC