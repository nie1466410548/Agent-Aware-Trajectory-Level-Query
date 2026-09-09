SELECT candidate_gender, COUNT(*) as cnt, 
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires
FROM greenhouse__application_enhanced 
WHERE candidate_gender IS NOT NULL
GROUP BY candidate_gender