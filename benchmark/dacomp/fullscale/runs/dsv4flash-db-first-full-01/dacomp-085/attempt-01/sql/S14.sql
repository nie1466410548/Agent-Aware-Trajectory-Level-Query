WITH subset AS (
  SELECT job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score,
    ROUND(current_employees_count*1.0/active_positions_count,4) AS talent_saturation,
    ROUND(high_performer_percentage*career_growth_potential_percentage,6) AS talent_quality_index
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1','Tier 2') AND talent_competition_level IN ('High','Very High')
)
SELECT 
  'health' AS metric,
  ROUND(MIN(job_health_score),2) AS p0, 
  ROUND(AVG(CASE WHEN rn_h <= cnt*0.25 THEN job_health_score END),2) AS q1,
  ROUND(AVG(CASE WHEN rn_h <= cnt*0.50 THEN job_health_score END),2) AS median,
  ROUND(AVG(CASE WHEN rn_h <= cnt*0.75 THEN job_health_score END),2) AS q3,
  ROUND(MAX(job_health_score),2) AS p100
FROM (
  SELECT job_health_score, ROW_NUMBER() OVER (ORDER BY job_health_score) AS rn_h, COUNT(*) OVER () AS cnt FROM subset
)
UNION ALL
SELECT 'dev',
  ROUND(MIN(avg_career_development_score),2),
  ROUND(AVG(CASE WHEN rn_d <= cnt*0.25 THEN avg_career_development_score END),2),
  ROUND(AVG(CASE WHEN rn_d <= cnt*0.50 THEN avg_career_development_score END),2),
  ROUND(AVG(CASE WHEN rn_d <= cnt*0.75 THEN avg_career_development_score END),2),
  ROUND(MAX(avg_career_development_score),2)
FROM (
  SELECT avg_career_development_score, ROW_NUMBER() OVER (ORDER BY avg_career_development_score) AS rn_d, COUNT(*) OVER () AS cnt FROM subset
)