SELECT 
  SUM(CASE WHEN "Benefits" LIKE '%Five social insurances%' THEN 1 ELSE 0 END) AS five_social,
  SUM(CASE WHEN "Benefits" LIKE '%housing provident fund%' OR "Benefits" LIKE '%housing fund%' THEN 1 ELSE 0 END) AS housing_fund,
  SUM(CASE WHEN "Benefits" LIKE '%commercial insurance%' THEN 1 ELSE 0 END) AS commercial_ins,
  SUM(CASE WHEN "Benefits" LIKE '%paid annual leave%' THEN 1 ELSE 0 END) AS annual_leave,
  SUM(CASE WHEN "Benefits" LIKE '%double pay at the end%' OR "Benefits" LIKE '%double salary at the end%' THEN 1 ELSE 0 END) AS double_pay,
  SUM(CASE WHEN "Benefits" LIKE '%performance bonus%' THEN 1 ELSE 0 END) AS perf_bonus,
  SUM(CASE WHEN "Benefits" LIKE '%year-end bonus%' OR "Benefits" LIKE '%year end bonus%' THEN 1 ELSE 0 END) AS year_end_bonus,
  SUM(CASE WHEN "Benefits" LIKE '%meal allowance%' OR "Benefits" LIKE '%meal subsidy%' OR "Benefits" LIKE '%food allowance%' THEN 1 ELSE 0 END) AS meal_allowance,
  SUM(CASE WHEN "Benefits" LIKE '%accommodation%' OR "Benefits" LIKE '%housing%' THEN 1 ELSE 0 END) AS accommodation,
  SUM(CASE WHEN "Benefits" LIKE '%meals provided%' OR "Benefits" LIKE '%meals and accommodation provided%' THEN 1 ELSE 0 END) AS meals_provided,
  SUM(CASE WHEN "Benefits" LIKE '%overtime pay%' THEN 1 ELSE 0 END) AS overtime_pay,
  SUM(CASE WHEN "Benefits" LIKE '%holiday benefits%' THEN 1 ELSE 0 END) AS holiday_benefits,
  SUM(CASE WHEN "Benefits" LIKE '%training%' THEN 1 ELSE 0 END) AS training,
  SUM(CASE WHEN "Benefits" LIKE '%travel%' THEN 1 ELSE 0 END) AS travel,
  SUM(CASE WHEN "Benefits" LIKE '%communication allowance%' OR "Benefits" LIKE '%communication subsidy%' THEN 1 ELSE 0 END) AS comm_allowance,
  SUM(CASE WHEN "Benefits" LIKE '%full attendance bonus%' OR "Benefits" LIKE '%attendance bonus%' THEN 1 ELSE 0 END) AS attendance_bonus,
  SUM(CASE WHEN "Benefits" LIKE '%high-temperature%' OR "Benefits" LIKE '%high temperature%' THEN 1 ELSE 0 END) AS high_temp,
  SUM(CASE WHEN "Benefits" LIKE '%shuttle%' THEN 1 ELSE 0 END) AS shuttle,
  SUM(CASE WHEN "Benefits" LIKE '%medical checkup%' OR "Benefits" LIKE '%physical examination%' THEN 1 ELSE 0 END) AS checkup,
  SUM(CASE WHEN "Benefits" LIKE '%work uniform%' OR "Benefits" LIKE '%uniform%' THEN 1 ELSE 0 END) AS uniform,
  SUM(CASE WHEN "Benefits" LIKE '%flexible working hours%' THEN 1 ELSE 0 END) AS flexible_hours
FROM sheet1 
WHERE "Education Requirement" = 'Vocational school or above' AND "Benefits" IS NOT NULL AND "Benefits" != ''