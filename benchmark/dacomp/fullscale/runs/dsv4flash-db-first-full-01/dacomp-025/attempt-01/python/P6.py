import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Create a detailed comparison for the two candidate items
# Show 2022 summer monthly avg profit for Gao Gua(1) and Gao Gua(2)

sql = """
WITH summer_analysis AS (
  SELECT s."Item Code",
    strftime('%Y-%m', s."Sales Date") as ym,
    strftime('%m', s."Sales Date") as mo,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Item Code" IN (102900005118824, 102900011032732)
    AND s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code", mo, COUNT(*) n, ROUND(AVG(profit),3) avg_profit,
  ROUND(AVG(up),2) avg_up, ROUND(AVG(wp/(1.0-lr/100.0)),2) avg_cost,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) pct_loss
FROM summer_analysis
GROUP BY "Item Code", mo
ORDER BY "Item Code", mo
"""
res = db.query(sql)
df = db.frame(res)
print(df.to_string())

# Also get the per-item names
sql2 = "SELECT \"Item Code\", \"Item Name\" FROM product_information WHERE \"Item Code\" IN (102900005118824, 102900011032732)"
res2 = db.query(sql2)
df2 = db.frame(res2)
print(df2.to_string())