SELECT retention_difficulty_level, 
  COUNT(*) AS cnt,
  ROUND(AVG(job_health_score),2) AS avg_health,
  ROUND(AVG(avg_career_development_score),2) AS avg_dev,
  ROUND(AVG(high_performer_percentage*career_growth_potential_percentage),5) AS avg_quality,
  ROUND(AVG(current_employees_count*1.0/active_positions_count),3) AS avg_saturation,
  ROUND(AVG(avg_weekly_hours),2) AS avg_hours,
  ROUND(SUM(is_work_shift_required)*1.0/COUNT(*),3) AS shift_ratio
FROM workday__job_overview
WHERE job_value_tier IN ('Tier 1','Tier 2') AND talent_competition_level IN ('High','Very High')
GROUP BY retention_difficulty_level
ORDER BY cnt DESC