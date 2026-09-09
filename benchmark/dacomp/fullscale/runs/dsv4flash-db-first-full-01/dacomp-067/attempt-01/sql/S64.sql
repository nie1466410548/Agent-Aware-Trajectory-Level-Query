
SELECT 
  CASE 
    WHEN lower(overall_recommendation) IN ('strong_yes','yes') THEN 'Positive'
    WHEN lower(overall_recommendation) IN ('strong_no','no','maybe') THEN 'Non-Positive'
    ELSE 'Other'
  END as rec_group,
  COUNT(*) as cnt
FROM greenhouse__interview_enhanced
WHERE overall_recommendation IS NOT NULL
GROUP BY rec_group
