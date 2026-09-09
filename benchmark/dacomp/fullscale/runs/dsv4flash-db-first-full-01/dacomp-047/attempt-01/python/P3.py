import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Check the result format
res = db.query("SELECT strftime('%Y-%m-%d', \"Sales Date\") AS d, pi.\"Category Name\" AS cat, SUM(\"Sales volume (kg)\") AS vol FROM sales_records s JOIN product_information pi ON s.\"Item Code\"=pi.\"Item Code\" GROUP BY d, cat")
print("Result keys:", res.keys())
print("Executions:", res['executions'][0].keys())
ex = res['executions'][0]
print("Columns:", ex['columns'])
print("Preview:", ex['preview'][:2])
print("Row count:", ex['row_count'])

# Now get rows
rows = db.rows(res)
print("First row:", rows[0])
print("Type:", type(rows[0]))