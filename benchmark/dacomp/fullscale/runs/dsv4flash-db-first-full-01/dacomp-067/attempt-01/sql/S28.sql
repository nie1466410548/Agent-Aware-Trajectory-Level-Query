SELECT candidate_gender, COUNT(*) as total, 
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
FROM greenhouse__application_enhanced 
GROUP BY candidate_gender