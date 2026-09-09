-- Caixi Strategy
SELECT
  s."Promotion Tertiary Category",
  MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) AS in_pre,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Caixi Strategy v4.8' THEN 1 ELSE 0 END) AS in_old_gray,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Caixi Strategy v4.9' THEN 1 ELSE 0 END) AS in_new_gray
FROM sheet1 s
WHERE s.Strategy IN ('Caixi Strategy v4.8','Caixi Strategy v4.9')
GROUP BY s."Promotion Tertiary Category"
ORDER BY s."Promotion Tertiary Category"