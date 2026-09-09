WITH base_metrics AS (
  SELECT
    job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score,
    retention_difficulty_level, is_work_shift_required, avg_weekly_hours,
    current_employees_count, active_positions_count,
    high_performer_percentage, career_growth_potential_percentage,
    ROUND(current_employees_count * 1.0 / active_positions_count, 4) AS talent_saturation,
    ROUND(high_performer_percentage * career_growth_potential_percentage, 6) AS talent_quality_index
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1', 'Tier 2')
)
SELECT 
  talent_competition_level,
  COUNT(*) AS cnt,
  ROUND(AVG(talent_saturation), 4) AS avg_saturation,
  ROUND(AVG(talent_quality_index), 6) AS avg_quality,
  ROUND(AVG(job_health_score), 2) AS avg_health,
  ROUND(AVG(avg_career_development_score), 2) AS avg_dev,
  ROUND(AVG(avg_weekly_hours), 2) AS avg_hours
FROM base_metrics
WHERE talent_competition_level IN ('High', 'Very High')
GROUP BY talent_competition_level