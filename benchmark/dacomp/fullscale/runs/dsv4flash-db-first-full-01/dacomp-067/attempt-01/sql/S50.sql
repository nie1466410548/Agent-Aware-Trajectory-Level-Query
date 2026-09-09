SELECT 
  ROUND(AVG(rating), 2) as avg_rating,
  ROUND(AVG(CASE WHEN overall_recommendation IN ('strong_yes','yes','Strong Yes','Yes') THEN rating END), 2) as avg_positive_rating,
  ROUND(AVG(CASE WHEN overall_recommendation IN ('strong_no','no','Strong No','No') THEN rating END), 2) as avg_negative_rating,
  ROUND(AVG(CASE WHEN overall_recommendation = 'Maybe' THEN rating END), 2) as avg_maybe_rating
FROM greenhouse__interview_scorecard_detail
WHERE rating IS NOT NULL