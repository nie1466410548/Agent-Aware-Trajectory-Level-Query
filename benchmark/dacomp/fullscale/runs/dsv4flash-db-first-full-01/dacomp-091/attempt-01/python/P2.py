import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# Check frame behavior
r = db.query("SELECT vendor_id, annual_spend_growth_pct FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7 LIMIT 3")
df_test = db.frame(r)
print(type(df_test))
print(df_test.head())
print(df_test.columns.tolist())