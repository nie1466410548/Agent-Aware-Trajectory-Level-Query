SELECT sourced_from,
       COUNT(*) as total_apps,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
       SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) as rejected,
       SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active,
       SUM(CASE WHEN status='withdrawn' THEN 1 ELSE 0 END) as withdrawn,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced 
GROUP BY sourced_from
ORDER BY hires DESC