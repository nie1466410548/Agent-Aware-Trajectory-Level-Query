SELECT
  SUM(CASE WHEN i.technical_score IS NULL THEN 1 ELSE 0 END) AS null_tech,
  SUM(CASE WHEN i.problem_solving_score IS NULL THEN 1 ELSE 0 END) AS null_ps,
  SUM(CASE WHEN i.communication_score IS NULL THEN 1 ELSE 0 END) AS null_comm,
  SUM(CASE WHEN i.overall_recommendation IS NULL THEN 1 ELSE 0 END) AS null_rec,
  SUM(CASE WHEN a.education_level IS NULL THEN 1 ELSE 0 END) AS null_edu,
  SUM(CASE WHEN a.years_of_experience IS NULL THEN 1 ELSE 0 END) AS null_yoe,
  SUM(CASE WHEN a.university_tier IS NULL THEN 1 ELSE 0 END) AS null_tier
FROM greenhouse__interview_enhanced i
LEFT JOIN greenhouse__application_enhanced a ON a.application_id = i.application_id