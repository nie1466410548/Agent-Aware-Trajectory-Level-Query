SELECT a.candidate_company, a.stage_offer, a.stage_hired, COUNT(*) AS n
FROM greenhouse__application_enhanced a
WHERE a.stage_technical_interview = 1
GROUP BY a.candidate_company, a.stage_offer, a.stage_hired
LIMIT 30