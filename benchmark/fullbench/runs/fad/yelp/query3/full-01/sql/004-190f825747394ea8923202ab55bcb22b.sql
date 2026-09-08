SELECT
  COUNT(DISTINCT CASE WHEN date LIKE '2018%' THEN business_ref END) AS n_like,
  COUNT(DISTINCT CASE WHEN date >= '2018-01-01' AND date < '2019-01-01' THEN business_ref END) AS n_range,
  MIN(date) AS min_date, MAX(date) AS max_date,
  SUM(CASE WHEN length(date) <> 10 THEN 1 ELSE 0 END) AS non_iso_dates
FROM review;

