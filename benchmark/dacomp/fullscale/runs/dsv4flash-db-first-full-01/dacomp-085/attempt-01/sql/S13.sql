WITH subset AS (
  SELECT job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score, retention_difficulty_level,
    is_work_shift_required, avg_weekly_hours, current_employees_count, active_positions_count,
    ROUND(current_employees_count*1.0/active_positions_count,4) AS talent_saturation,
    ROUND(high_performer_percentage*career_growth_potential_percentage,6) AS talent_quality_index
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1','Tier 2') AND talent_competition_level IN ('High','Very High')
)
SELECT 
  ROUND(AVG(job_health_score),2) AS mean_health, 
  MIN(job_health_score) AS min_health, MAX(job_health_score) AS max_health,
  ROUND(AVG(avg_career_development_score),2) AS mean_dev,
  MIN(avg_career_development_score) AS min_dev, MAX(avg_career_development_score) AS max_dev,
  ROUND(AVG(talent_saturation),3) AS mean_sat,
  ROUND(AVG(talent_quality_index),5) AS mean_quality
FROM subset