SELECT
  MIN("Completion Quality Score") AS min_q,
  MAX("Completion Quality Score") AS max_q
FROM sheet1 WHERE "Completion Quality Score" != '-'