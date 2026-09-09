SELECT sourced_from,
       SUM(CASE WHEN candidate_gender='Female' AND status='hired' THEN 1 ELSE 0 END) as female_hires,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as total_hires_with_gender,
       ROUND(100.0 * SUM(CASE WHEN candidate_gender='Female' AND status='hired' THEN 1 ELSE 0 END) / 
             NULLIF(SUM(CASE WHEN candidate_gender IS NOT NULL AND status='hired' THEN 1 ELSE 0 END), 0), 1) as female_pct
FROM greenhouse__application_enhanced 
GROUP BY sourced_from