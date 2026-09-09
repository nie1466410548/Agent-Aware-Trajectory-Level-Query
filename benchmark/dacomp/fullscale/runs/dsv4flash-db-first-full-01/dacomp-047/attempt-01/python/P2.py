import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Check the data
cats = db.rows(db.query("SELECT strftime('%Y-%m-%d', \"Sales Date\") AS d, pi.\"Category Name\" AS cat, SUM(\"Sales volume (kg)\") AS vol FROM sales_records s JOIN product_information pi ON s.\"Item Code\"=pi.\"Item Code\" GROUP BY d, cat"))
print("cats type:", type(cats))
print("cats first element:", cats[0] if cats else "empty")
print("cats keys:", cats[0].keys() if cats else "empty")

cat_df = pd.DataFrame(cats)
print("cat_df columns:", cat_df.columns.tolist())
print("cat_df head:\n", cat_df.head())