SELECT candidate_gender, candidate_race, COUNT(*) as cnt 
FROM greenhouse__application_enhanced 
WHERE status = 'hired'
GROUP BY candidate_gender, candidate_race
ORDER BY cnt DESC