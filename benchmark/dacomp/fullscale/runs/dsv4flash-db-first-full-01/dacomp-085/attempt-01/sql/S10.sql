SELECT job_value_tier, 
  AVG(job_health_score) AS avg_health, AVG(avg_career_development_score) AS avg_dev,
  AVG(high_performer_percentage) AS avg_hp, AVG(career_growth_potential_percentage) AS avg_cgp,
  AVG(current_employees_count*1.0/active_positions_count) AS avg_saturation
FROM workday__job_overview GROUP BY job_value_tier