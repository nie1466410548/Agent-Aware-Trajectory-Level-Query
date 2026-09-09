WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year, s1."Customer ID" AS cid
  FROM sheet1 s1
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Segment, year, COUNT(DISTINCT cid) AS customers,
       ROUND(100.0*COUNT(DISTINCT cid)/SUM(COUNT(DISTINCT cid)) OVER (PARTITION BY year),1) AS segment_customer_share_pct
FROM base GROUP BY Segment, year
ORDER BY Segment, year