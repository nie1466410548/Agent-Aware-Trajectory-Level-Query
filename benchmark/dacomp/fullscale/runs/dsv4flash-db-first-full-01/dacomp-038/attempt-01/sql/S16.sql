SELECT s."Promotion Date",
  COUNT(DISTINCT s."Promotion Tertiary Category") AS n_cats_old,
  (SELECT COUNT(DISTINCT "Promotion Tertiary Category") FROM sheet1 WHERE Strategy='Search Strategy v3.6' AND "Promotion Date"='2025-07-01') AS n_cats_jul1
FROM sheet1 s WHERE s.Strategy='Search Strategy v3.6' AND s."Promotion Date" BETWEEN '2025-07-04' AND '2025-07-07'
GROUP BY s."Promotion Date"