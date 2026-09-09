WITH all_rows AS (
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced" AS units,
         CAST(REPLACE("Pass Rate", '%','') AS REAL) AS pass_pct,
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0 AS eff_hours,
         "Disciplinary Issue"
  FROM sheet1
  UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet2
  UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet3
  UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet4
  UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet5
  UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet6
)
SELECT "Employee ID", "Employee", Team, "Gender", Age, "Education Level", "Hire Date",
       COUNT(*) AS days,
       ROUND(SUM(eff_hours),2) AS total_eff_hours,
       ROUND(AVG(eff_hours),3) AS avg_eff_hours,
       ROUND(SUM(units),1) AS total_units,
       ROUND(AVG(units),2) AS avg_units,
       ROUND(AVG(pass_pct),2) AS avg_pass_rate,
       SUM(CASE WHEN "Disciplinary Issue"='Yes' THEN 1 ELSE 0 END) AS discipline_days
FROM all_rows
GROUP BY "Employee ID", "Employee", Team, "Gender", Age, "Education Level", "Hire Date"
ORDER BY total_units DESC