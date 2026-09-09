SELECT attribute_category, COUNT(*) as cnt, 
       AVG(rating) as avg_rating
FROM greenhouse__interview_scorecard_detail
GROUP BY attribute_category
ORDER BY cnt DESC