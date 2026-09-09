-- Popup Strategy
SELECT
  s."Promotion Tertiary Category",
  MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) AS in_pre,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Popup Strategy v2.9' THEN 1 ELSE 0 END) AS in_old_gray,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Popup Strategy v2.9.1' THEN 1 ELSE 0 END) AS in_new_gray
FROM sheet1 s
WHERE s.Strategy IN ('Popup Strategy v2.9','Popup Strategy v2.9.1')
GROUP BY s."Promotion Tertiary Category"
ORDER BY s."Promotion Tertiary Category"