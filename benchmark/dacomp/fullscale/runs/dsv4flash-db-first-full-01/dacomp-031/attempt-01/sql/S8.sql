SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years (Long-term)' ELSE '<10 years' END AS tenure_group,
  COUNT(*) AS cnt,
  ROUND(AVG(Age),2) AS avg_age,
  ROUND(AVG(MonthlyIncome),2) AS avg_monthly_income,
  ROUND(AVG(PercentSalaryHike),2) AS avg_salary_hike,
  ROUND(AVG(JobSatisfaction),2) AS avg_job_satisfaction,
  ROUND(AVG(EnvironmentSatisfaction),2) AS avg_env_satisfaction,
  ROUND(AVG(WorkLifeBalance),2) AS avg_work_life_balance,
  ROUND(AVG(JobInvolvement),2) AS avg_job_involvement,
  ROUND(AVG(RelationshipSatisfaction),2) AS avg_rel_satisfaction,
  ROUND(AVG(PerformanceRating),2) AS avg_perf_rating,
  ROUND(AVG(StockOptionLevel),2) AS avg_stock_option,
  ROUND(AVG(TrainingTimesLastYear),2) AS avg_training,
  ROUND(AVG(DistanceFromHome),2) AS avg_distance,
  ROUND(AVG(NumCompaniesWorked),2) AS avg_num_companies,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(YearsInCurrentRole),2) AS avg_years_in_role,
  ROUND(AVG(YearsWithCurrManager),2) AS avg_years_with_mgr
FROM sheet1
GROUP BY tenure_group