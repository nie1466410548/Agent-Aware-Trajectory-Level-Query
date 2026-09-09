import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = db.frame(db.query("""
  SELECT "Carat (diamond weight)" AS carat, "Cut (quality)" AS cut, "Color" AS color,
         "Clarity" AS clarity, "Depth percentage" AS depth, "Table percentage" AS tbl,
         "Price (USD)" AS price
  FROM sheet1
"""))
print(df.shape)
print(df.dtypes)
print(df.isna().sum())
df.to_json('/work/diamonds_analysis.json', orient='records')
print("saved")
