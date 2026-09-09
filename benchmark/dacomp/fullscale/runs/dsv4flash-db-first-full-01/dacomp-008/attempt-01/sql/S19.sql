WITH dev AS (
  SELECT 
    "Project Type",
    "Budget Amount" - "Actual Cost" AS deviation
  FROM sheet1
),
ranked AS (
  SELECT 
    "Project Type",
    deviation,
    ROW_NUMBER() OVER (PARTITION BY "Project Type" ORDER BY deviation) as rn,
    COUNT(*) OVER (PARTITION BY "Project Type") as cnt
  FROM dev
)
SELECT 
  "Project Type",
  MAX(CASE WHEN rn <= CAST(cnt*0.10 AS INTEGER) THEN deviation END) as p10,
  MAX(CASE WHEN rn <= CAST(cnt*0.25 AS INTEGER) THEN deviation END) as p25,
  MAX(CASE WHEN rn <= CAST(cnt*0.50 AS INTEGER) THEN deviation END) as p50,
  MAX(CASE WHEN rn <= CAST(cnt*0.75 AS INTEGER) THEN deviation END) as p75,
  MAX(CASE WHEN rn <= CAST(cnt*0.90 AS INTEGER) THEN deviation END) as p90
FROM ranked
GROUP BY "Project Type"