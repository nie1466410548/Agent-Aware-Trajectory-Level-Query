SELECT 
  COUNT(*) AS total,
  SUM(CASE WHEN active_positions_count IS NULL OR active_positions_count = 0 THEN 1 ELSE 0 END) AS zero_active_pos,
  SUM(CASE WHEN current_employees_count IS NULL THEN 1 ELSE 0 END) AS null_curr_emp,
  SUM(CASE WHEN high_performer_percentage IS NULL THEN 1 ELSE 0 END) AS null_hp,
  SUM(CASE WHEN career_growth_potential_percentage IS NULL THEN 1 ELSE 0 END) AS null_cgp,
  SUM(CASE WHEN job_health_score IS NULL THEN 1 ELSE 0 END) AS null_jhs,
  SUM(CASE WHEN avg_career_development_score IS NULL THEN 1 ELSE 0 END) AS null_ads,
  MIN(active_positions_count) AS min_active,
  MAX(active_positions_count) AS max_active
FROM workday__job_overview