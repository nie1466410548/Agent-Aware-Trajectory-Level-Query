import pandas as pd
import numpy as np

res = db.query("SELECT * FROM \"2000_cn_pop_6_up_age_sex_edu\"")
df2000 = db.frame(res)
print("2000 columns:", df2000.columns.tolist())
print("2000 shape:", df2000.shape)
print(df2000.head(2))