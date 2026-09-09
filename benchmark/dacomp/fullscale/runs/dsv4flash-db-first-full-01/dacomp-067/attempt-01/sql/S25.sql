SELECT COUNT(*) as total_hires,
       SUM(CASE WHEN candidate_gender = 'Female' THEN 1 ELSE 0 END) as female_hires,
       ROUND(100.0 * SUM(CASE WHEN candidate_gender = 'Female' THEN 1 ELSE 0 END) / COUNT(*), 1) as female_pct,
       SUM(CASE WHEN candidate_race != 'White' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END) as non_white_hires,
       ROUND(100.0 * SUM(CASE WHEN candidate_race != 'White' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) as non_white_pct
FROM greenhouse__application_enhanced 
WHERE status = 'hired'