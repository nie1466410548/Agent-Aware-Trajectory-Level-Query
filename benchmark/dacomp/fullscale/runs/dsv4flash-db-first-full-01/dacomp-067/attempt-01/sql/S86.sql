
SELECT 
  CASE 
    WHEN lower(overall_recommendation) IN ('strong_yes', 'strong yes') THEN 5
    WHEN lower(overall_recommendation) IN ('yes') THEN 4
    WHEN lower(overall_recommendation) IN ('maybe') THEN 3
    WHEN lower(overall_recommendation) IN ('no') THEN 2
    WHEN lower(overall_recommendation) IN ('strong_no', 'strong no') THEN 1
    ELSE NULL
  END as rec_score,
  COUNT(*) as cnt
FROM greenhouse__interview_enhanced
WHERE overall_recommendation IS NOT NULL
GROUP BY rec_score
ORDER BY rec_score
