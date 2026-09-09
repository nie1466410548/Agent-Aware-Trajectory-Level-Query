WITH all_rows AS (
  SELECT "Gender", "Away-from-Station Count" AS away_cnt FROM sheet1
  UNION ALL SELECT "Gender", "Away-from-Station Count" FROM sheet2
  UNION ALL SELECT "Gender", "Away-from-Station Count" FROM sheet3
  UNION ALL SELECT "Gender", "Away-from-Station Count" FROM sheet4
  UNION ALL SELECT "Gender", "Away-from-Station Count" FROM sheet5
  UNION ALL SELECT "Gender", "Away-from-Station Count" FROM sheet6
)
SELECT "Gender", COUNT(*) AS records,
       ROUND(AVG(away_cnt),2) AS avg_away_cnt,
       ROUND(MIN(away_cnt),1) AS min_away,
       ROUND(MAX(away_cnt),1) AS max_away
FROM all_rows GROUP BY "Gender"