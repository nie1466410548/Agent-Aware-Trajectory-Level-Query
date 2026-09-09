WITH all_rows AS (
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced" AS units,
         CAST(REPLACE("Pass Rate", '%','') AS REAL) AS pass_pct,
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0 AS eff_hours,
         "Disciplinary Issue"
  FROM sheet1 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet2 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet3 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet4 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet5 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet6
),
emp_agg AS (
  SELECT "Employee ID", "Employee", Team, "Gender", Age, "Education Level",
         MAX(CAST(REPLACE("Hire Date",' months','') AS INTEGER)) AS tenure_months,
         COUNT(*) AS days,
         SUM(eff_hours) AS total_eff_hours,
         SUM(units) AS total_units,
         AVG(units) AS avg_units,
         AVG(pass_pct) AS avg_pass_rate,
         SUM(CASE WHEN "Disciplinary Issue"='Yes' THEN 1 ELSE 0 END) AS discipline_days
  FROM all_rows
  GROUP BY "Employee ID", "Employee", Team, "Gender", Age, "Education Level"
)
SELECT *,
       ROUND(( (total_eff_hours - min_eh) / (max_eh - min_eh) +
               (total_units - min_tu) / (max_tu - min_tu) +
               (avg_pass_rate - min_pr) / (max_pr - min_pr) ) / 3.0, 4) AS composite_score,
       RANK() OVER (ORDER BY ( (total_eff_hours - min_eh) / (max_eh - min_eh) +
                               (total_units - min_tu) / (max_tu - min_tu) +
                               (avg_pass_rate - min_pr) / (max_pr - min_pr) ) / 3.0 DESC) AS rank
FROM emp_agg
CROSS JOIN (SELECT MIN(total_eff_hours) AS min_eh, MAX(total_eff_hours) AS max_eh,
                   MIN(total_units) AS min_tu, MAX(total_units) AS max_tu,
                   MIN(avg_pass_rate) AS min_pr, MAX(avg_pass_rate) AS max_pr
            FROM emp_agg)
ORDER BY composite_score DESC
LIMIT 25