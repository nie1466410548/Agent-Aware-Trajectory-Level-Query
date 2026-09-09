
import numpy as np, pandas as pd
from scipy import stats

res = db.query("SELECT * FROM sheet1")
df = db.frame(res)
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
df.to_csv('work/sheet1_full.csv', index=False)
