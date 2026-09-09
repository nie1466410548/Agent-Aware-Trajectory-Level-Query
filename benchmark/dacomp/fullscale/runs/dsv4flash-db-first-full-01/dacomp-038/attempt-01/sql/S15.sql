SELECT s."Promotion Date", s."Promotion Tertiary Category",
  MAX(CASE WHEN s.Strategy='Search Strategy v3.6' THEN 1 ELSE 0 END) AS has_old,
  MAX(CASE WHEN s.Strategy='Search Strategy v3.7' THEN 1 ELSE 0 END) AS has_new
FROM sheet1 s
WHERE s.Strategy IN ('Search Strategy v3.6','Search Strategy v3.7') AND s."Promotion Date" >= '2025-07-04'
GROUP BY s."Promotion Date", s."Promotion Tertiary Category"
ORDER BY s."Promotion Date", s."Promotion Tertiary Category"