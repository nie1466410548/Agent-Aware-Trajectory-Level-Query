WITH all_rows AS (
  SELECT "Employee ID", "Gender", "Units Produced" AS units,
         "Away-from-Station Count" AS away_cnt,
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0 AS eff_hours
  FROM sheet1 UNION ALL
  SELECT "Employee ID", "Gender", "Units Produced",
         "Away-from-Station Count",
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0
  FROM sheet2 UNION ALL
  SELECT "Employee ID", "Gender", "Units Produced",
         "Away-from-Station Count",
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0
  FROM sheet3 UNION ALL
  SELECT "Employee ID", "Gender", "Units Produced",
         "Away-from-Station Count",
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0
  FROM sheet4 UNION ALL
  SELECT "Employee ID", "Gender", "Units Produced",
         "Away-from-Station Count",
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0
  FROM sheet5 UNION ALL
  SELECT "Employee ID", "Gender", "Units Produced",
         "Away-from-Station Count",
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0
  FROM sheet6
)
SELECT "Gender",
       ROUND(AVG(units),2) AS avg_units_per_day,
       ROUND(AVG(eff_hours),3) AS avg_eff_hours_per_day,
       ROUND(AVG(away_cnt),2) AS avg_away_count,
       ROUND(AVG(8.0 - eff_hours),2) AS avg_time_away_hours,
       COUNT(*) AS records
FROM all_rows
GROUP BY "Gender"