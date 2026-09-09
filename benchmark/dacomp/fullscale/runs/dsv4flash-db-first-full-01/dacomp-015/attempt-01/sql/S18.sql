SELECT COUNT(*) AS total,
  SUM(CASE WHEN "Watch Count" > 0 THEN 1 ELSE 0 END) AS watch_gt0,
  SUM(CASE WHEN "Watch Count" = 0 THEN 1 ELSE 0 END) AS watch_eq0,
  SUM(CASE WHEN "Watch Count" > 50 THEN 1 ELSE 0 END) AS watch_gt50,
  SUM(CASE WHEN "Showings" > 0 THEN 1 ELSE 0 END) AS show_gt0,
  SUM(CASE WHEN "Showings" = 0 THEN 1 ELSE 0 END) AS show_eq0,
  SUM(CASE WHEN "Showings" > 10 THEN 1 ELSE 0 END) AS show_gt10,
  AVG("Watch Count") AS avg_watch, AVG(Showings) AS avg_show,
  MAX("Watch Count") AS max_watch, MAX(Showings) AS max_show,
  MIN("Watch Count") AS min_watch, MIN(Showings) AS min_show
FROM data