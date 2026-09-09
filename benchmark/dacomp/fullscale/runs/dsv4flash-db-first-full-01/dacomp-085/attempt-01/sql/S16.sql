WITH base AS (
  SELECT
    job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score,
    retention_difficulty_level, is_work_shift_required, avg_weekly_hours,
    current_employees_count, active_positions_count, total_positions_count,
    high_performer_percentage, career_growth_potential_percentage,
    ROUND(current_employees_count * 1.0 / NULLIF(active_positions_count, 0), 4) AS talent_saturation,
    ROUND(high_performer_percentage * career_growth_potential_percentage, 6) AS talent_quality_index,
    job_rarity_level, job_maturity_level, talent_management_recommendation
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1', 'Tier 2') AND talent_competition_level IN ('High', 'Very High')
)
SELECT * FROM base
ORDER BY job_health_score ASC, avg_career_development_score ASC
LIMIT 30