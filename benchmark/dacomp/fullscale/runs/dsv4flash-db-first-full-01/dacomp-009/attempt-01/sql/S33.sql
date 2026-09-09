WITH all_rows AS (
  SELECT "Employee ID", "Date",
         substr(Date,1,7) AS month,
         "Units Produced" AS units,
         CAST(REPLACE("Pass Rate", '%','') AS REAL) AS pass_pct
  FROM sheet1 UNION ALL
  SELECT "Employee ID", Date, substr(Date,1,7), "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL) FROM sheet2 UNION ALL
  SELECT "Employee ID", Date, substr(Date,1,7), "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL) FROM sheet3 UNION ALL
  SELECT "Employee ID", Date, substr(Date,1,7), "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL) FROM sheet4 UNION ALL
  SELECT "Employee ID", Date, substr(Date,1,7), "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL) FROM sheet5 UNION ALL
  SELECT "Employee ID", Date, substr(Date,1,7), "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL) FROM sheet6
)
SELECT "Employee ID", month, COUNT(*) AS days, ROUND(SUM(units),1) AS units, ROUND(AVG(pass_pct),2) AS pass_rate
FROM all_rows GROUP BY "Employee ID", month
ORDER BY "Employee ID", month