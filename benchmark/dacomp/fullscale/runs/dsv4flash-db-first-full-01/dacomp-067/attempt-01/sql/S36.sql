SELECT COUNT(*) as total_scores, 
       AVG(rating) as avg_rating,
       MIN(rating) as min_rating,
       MAX(rating) as max_rating
FROM greenhouse__interview_scorecard_detail