SELECT MIN(date) AS min_date, MAX(date) AS max_date, COUNT(*) AS total,
       COUNT(*) FILTER (WHERE date >= '2016-01-01' AND date < '2016-07-01') AS in_window
FROM review;

