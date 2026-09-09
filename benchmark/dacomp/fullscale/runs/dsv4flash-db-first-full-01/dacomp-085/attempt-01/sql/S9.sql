SELECT
  MIN(high_performer_percentage) AS min_hp, MAX(high_performer_percentage) AS max_hp, AVG(high_performer_percentage) AS avg_hp,
  MIN(career_growth_potential_percentage) AS min_cgp, MAX(career_growth_potential_percentage) AS max_cgp, AVG(career_growth_potential_percentage) AS avg_cgp,
  MIN(job_health_score) AS min_jhs, MAX(job_health_score) AS max_jhs, AVG(job_health_score) AS avg_jhs,
  MIN(avg_career_development_score) AS min_ads, MAX(avg_career_development_score) AS max_ads, AVG(avg_career_development_score) AS avg_ads,
  MIN(current_employees_count) AS min_ce, MAX(current_employees_count) AS max_ce,
  MIN(avg_weekly_hours) AS min_wk, MAX(avg_weekly_hours) AS max_wk
FROM workday__job_overview