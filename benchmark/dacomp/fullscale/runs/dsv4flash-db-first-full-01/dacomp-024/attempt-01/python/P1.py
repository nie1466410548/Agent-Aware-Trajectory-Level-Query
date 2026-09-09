
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load aggregated region-segment-year data (S15 result) via logged query
res = db.query("""
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Customer ID" AS cid, s1."Order ID" AS oid,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
       COUNT(DISTINCT cid) AS customers, COUNT(DISTINCT oid) AS orders
FROM base GROUP BY Region, Segment, year
ORDER BY year, Region, Segment
""")
df = db.frame(res)
print(df.shape)
print(df.head())
