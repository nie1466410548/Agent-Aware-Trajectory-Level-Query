WITH subset AS (
  SELECT job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score, retention_difficulty_level,
    is_work_shift_required, avg_weekly_hours, current_employees_count, active_positions_count,
    ROUND(current_employees_count*1.0/active_positions_count,4) AS talent_saturation,
    ROUND(high_performer_percentage*career_growth_potential_percentage,6) AS talent_quality_index
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1','Tier 2') AND talent_competition_level IN ('High','Very High')
)
SELECT * FROM subset ORDER BY job_profile_id