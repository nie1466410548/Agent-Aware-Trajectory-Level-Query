SELECT
  CASE
    WHEN "Date" ~ '^[0-9]{2} [A-Za-z]{3} [0-9]{4}' THEN 'DD Mon YYYY'
    WHEN "Date" ~ '^[A-Za-z]+ [0-9]{1,2}, [0-9]{4}' THEN 'Month D, YYYY'
    ELSE 'OTHER'
  END AS fmt,
  COUNT(*) AS n,
  MIN("Date") AS ex1
FROM index_trade
GROUP BY fmt;

