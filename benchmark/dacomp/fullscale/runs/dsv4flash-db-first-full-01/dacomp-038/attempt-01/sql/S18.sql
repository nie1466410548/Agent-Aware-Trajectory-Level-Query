SELECT
  s."Promotion Tertiary Category",
  MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) AS in_pre,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Search Strategy v3.6' THEN 1 ELSE 0 END) AS in_old_gray,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Search Strategy v3.7' THEN 1 ELSE 0 END) AS in_new_gray
FROM sheet1 s
WHERE s.Strategy IN ('Search Strategy v3.6','Search Strategy v3.7')
GROUP BY s."Promotion Tertiary Category"
ORDER BY s."Promotion Tertiary Category"