SELECT status, COUNT(*) as cnt, 
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM greenhouse__interview_enhanced), 1) as pct
FROM greenhouse__interview_enhanced
GROUP BY status
ORDER BY cnt DESC