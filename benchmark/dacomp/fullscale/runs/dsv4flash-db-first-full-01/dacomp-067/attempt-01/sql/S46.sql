SELECT sourced_from,
       SUM(CASE WHEN candidate_race != 'White' AND candidate_race IS NOT NULL AND status='hired' THEN 1 ELSE 0 END) as non_white_hires,
       SUM(CASE WHEN status='hired' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END) as total_hires_with_race,
       ROUND(100.0 * SUM(CASE WHEN candidate_race != 'White' AND candidate_race IS NOT NULL AND status='hired' THEN 1 ELSE 0 END) / 
             NULLIF(SUM(CASE WHEN status='hired' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END), 0), 1) as non_white_pct
FROM greenhouse__application_enhanced 
GROUP BY sourced_from