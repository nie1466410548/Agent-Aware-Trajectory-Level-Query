WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year, s1."Customer ID" AS cid
  FROM sheet1 s1
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, year, COUNT(DISTINCT cid) AS customers,
       ROUND(100.0*COUNT(DISTINCT cid)/SUM(COUNT(DISTINCT cid)) OVER (PARTITION BY year),1) AS customer_share_pct
FROM base GROUP BY Region, year
ORDER BY year, customers DESC