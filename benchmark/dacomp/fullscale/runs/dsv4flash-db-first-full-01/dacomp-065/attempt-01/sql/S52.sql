
SELECT DISTINCT a.application_id, a.candidate_gender, a.candidate_race, 
       a.candidate_disability_status, a.candidate_veteran_status,
       a.stage_offer, a.stage_hired, a.status
FROM greenhouse__application_enhanced a
