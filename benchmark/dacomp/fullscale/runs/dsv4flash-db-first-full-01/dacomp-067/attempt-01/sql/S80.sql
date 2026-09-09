
SELECT scorecard_id, 
       AVG(rating) as avg_scorecard_rating,
       MAX(rating) as max_rating,
       MIN(rating) as min_rating,
       overall_recommendation
FROM greenhouse__interview_scorecard_detail
WHERE rating IS NOT NULL
GROUP BY scorecard_id
